"""
PDF report exporter — professional government-format layout.

Key design decisions:
  - All layout happens in figure-fraction coordinates (origin = bottom-left).
  - Dynamic row heights: each table row is tall enough for its wrapped content.
  - Pre-calculated pagination: blocks are assembled as a list of draw-commands
    and distributed across pages before any rendering happens.
  - Consistent 0.08 left / 0.92 right margins on EVERY page.
"""

import io
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from .base import BaseReportExporter

# ── Design tokens ─────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = 8.5, 11.0   # inches

ML = 0.08                     # left margin (figure fraction)
MR = 0.92                     # right margin
CW = MR - ML                  # content width (0.84)

FOOTER_TOP  = 0.055           # top of footer rule
HEADER_BOT  = 0.95            # first usable y on a region page
TOP_Y       = 0.93

# Typography
FS_H1   = 14   # region heading
FS_H2   = 9    # section title
FS_BODY = 8
FS_CELL = 7.5
FS_FOOT = 6.5

# Colours
C_ACCENT   = "#15803d"
C_DARK     = "#1c1917"
C_MUTED    = "#57534e"
C_TH_BG    = "#15803d"        # table header background (green)
C_TH_FG    = "#ffffff"        # table header text
C_ROW_ODD  = "#ffffff"
C_ROW_EVEN = "#f0fdf4"        # very light green
C_BORDER   = "#cbd5e1"
C_RULE     = "#15803d"

# Spacing
LINE_H    = 0.018   # one text line at FS_CELL
HDR_H     = 0.028   # fixed table-header row height
CELL_PX   = 0.006   # vertical padding inside each data cell (each side)
TITLE_H   = 0.028   # space for a section title + gap below
SECTION_GAP = 0.018
BODY_LEAD   = 0.016  # leading for body / description text


# ── Helpers ───────────────────────────────────────────────────────────────────

def _wrap(text, col_frac):
    """Split *text* into lines that fit in a column whose width is
    *col_frac* × CW of the page."""
    if not text:
        return [""]
    width_in = PAGE_W * CW * col_frac
    chars = max(6, int(width_in / 0.055))   # DejaVu Sans 7.5 pt ≈ 0.055 in/char
    return textwrap.wrap(str(text), width=chars) or [str(text)]


def _row_h(row, col_fracs):
    """Dynamic height for one data row (accounts for wrapped content)."""
    max_lines = 1
    for val, cf in zip(row, col_fracs):
        max_lines = max(max_lines, len(_wrap(str(val), cf)))
    return max_lines * LINE_H + CELL_PX * 2


def _table_h(rows, col_fracs):
    """Total height consumed by a titled table."""
    h = TITLE_H + HDR_H
    for row in rows:
        h += _row_h(row, col_fracs)
    return h + SECTION_GAP


# ── Exporter ──────────────────────────────────────────────────────────────────

class PdfReportExporter(BaseReportExporter):
    format_name = "pdf"

    # ── Low-level figure helpers ───────────────────────────────────────────

    def _new_fig(self):
        fig = plt.figure(figsize=(PAGE_W, PAGE_H))
        fig.patch.set_facecolor("white")
        return fig

    def _ft(self, fig, x, y, s, **kw):
        """Place text in figure-fraction coords, top-left origin (y decreases downward)."""
        fig.text(x, y, s, transform=fig.transFigure,
                 va=kw.pop("va", "top"), ha=kw.pop("ha", "left"), **kw)

    def _hline(self, fig, y, x0=ML, x1=MR, color=C_BORDER, lw=0.5):
        fig.add_artist(plt.Line2D([x0, x1], [y, y],
                                  transform=fig.transFigure,
                                  color=color, linewidth=lw, clip_on=False))

    def _rect(self, fig, x, y, w, h, fc, ec=C_BORDER, lw=0.3):
        """Draw a filled rectangle; (x, y) = top-left corner in fig-fractions."""
        p = mpatches.FancyBboxPatch(
            (x, y - h), w, h,
            boxstyle="square,pad=0",
            facecolor=fc, edgecolor=ec, linewidth=lw,
            transform=fig.transFigure, clip_on=False)
        fig.add_artist(p)

    # ── Page-level chrome ─────────────────────────────────────────────────

    def _draw_footer(self, fig, report_id, page_num, generated_at):
        self._hline(fig, FOOTER_TOP + 0.010, color=C_BORDER, lw=0.4)
        self._ft(fig, ML, FOOTER_TOP,
                 f"Report ID: {report_id}  ·  Page {page_num}  ·  {generated_at}",
                 fontsize=FS_FOOT, color=C_MUTED, va="bottom")
        self._ft(fig, MR, FOOTER_TOP,
                 "Urban Heat Island Intelligence Programme — Bangladesh",
                 fontsize=FS_FOOT, color=C_MUTED, ha="right", va="bottom")

    def _draw_region_heading(self, fig, y, region_name, description):
        """Draws region heading + green rule + description; returns new y."""
        # Green accent bar
        self._rect(fig, ML, y, CW, 0.032, fc=C_ACCENT, ec="none")
        self._ft(fig, ML + 0.012, y - 0.003,
                 f"Region: {region_name}",
                 fontsize=FS_H1, fontweight="bold", color="white", va="top")
        y -= 0.042   # below the bar

        if description:
            lines = textwrap.wrap(description, width=110)
            for line in lines:
                self._ft(fig, ML, y, line, fontsize=FS_BODY, color=C_MUTED, va="top")
                y -= BODY_LEAD
            y -= 0.008

        return y

    # ── Table drawing ─────────────────────────────────────────────────────

    def _draw_table(self, fig, y, title, col_headers, col_fracs, rows):
        """
        Draw a titled table on *fig* starting at figure-fraction y (top edge).
        Returns the y position after the table.

        col_fracs: list of floats summing to 1.0 (fractions of CW)
        """
        # Section title with subtle left accent bar
        self._rect(fig, ML, y, 0.004, TITLE_H - 0.004, fc=C_ACCENT, ec="none")
        self._ft(fig, ML + 0.012, y,
                 title, fontsize=FS_H2, fontweight="bold", color=C_DARK, va="top")
        y -= TITLE_H

        abs_widths = [cf * CW for cf in col_fracs]

        # ── Header row ────────────────────────────────────────────────────
        x = ML
        for header, aw in zip(col_headers, abs_widths):
            self._rect(fig, x, y, aw, HDR_H, fc=C_TH_BG, ec=C_BORDER, lw=0.3)
            self._ft(fig, x + 0.010, y - HDR_H / 2,
                     header, fontsize=FS_CELL, fontweight="bold",
                     color=C_TH_FG, va="center")
            x += aw
        y -= HDR_H

        # ── Data rows ─────────────────────────────────────────────────────
        for ri, row in enumerate(rows):
            rh = _row_h(row, col_fracs)
            bg = C_ROW_ODD if ri % 2 == 0 else C_ROW_EVEN

            x = ML
            for ci, (cell_val, cf, aw) in enumerate(zip(row, col_fracs, abs_widths)):
                self._rect(fig, x, y, aw, rh, fc=bg, ec=C_BORDER, lw=0.2)

                # Wrap text and draw each line
                lines = _wrap(str(cell_val), cf)
                line_y = y - CELL_PX
                for line in lines:
                    self._ft(fig, x + 0.008, line_y,
                             line, fontsize=FS_CELL, color=C_DARK, va="top")
                    line_y -= LINE_H
                x += aw

            y -= rh

        y -= SECTION_GAP
        return y

    # ── Content builders ──────────────────────────────────────────────────

    def _stat_rows(self, stats, keys_labels, fmt=".2f"):
        return [[label, f"{stats.get(key, 0):{fmt}}"]
                for key, label in keys_labels]

    # ── Main export ───────────────────────────────────────────────────────

    def export(self, report_document):
        buffer     = io.BytesIO()
        report_id  = report_document.get("reportId", "N/A")
        gen_at     = report_document.get("generatedAt", "")
        regions_s  = ", ".join(report_document.get("regions", []))
        sections   = report_document.get("sections", [])

        all_figs  = []
        page_num  = 1

        # ── Cover page ────────────────────────────────────────────────────
        fig = self._new_fig()

        # Header band
        self._rect(fig, 0, 1.0, 1.0, 0.14, fc=C_ACCENT, ec="none")
        self._ft(fig, 0.5, 0.97,
                 "PEOPLE'S REPUBLIC OF BANGLADESH",
                 fontsize=15, fontweight="bold", color="white", ha="center")
        self._ft(fig, 0.5, 0.92,
                 "Ministry of Environment  ·  Forest and Climate Change",
                 fontsize=10, color="#d1fae5", ha="center")
        self._ft(fig, 0.5, 0.88,
                 "Urban Heat Island Intelligence Programme",
                 fontsize=10, color="#d1fae5", ha="center")

        # Title box
        self._rect(fig, ML, 0.78, CW, 0.10, fc="#f0fdf4", ec=C_ACCENT, lw=1.0)
        title = report_document.get("title", "Environmental Report")
        self._ft(fig, 0.5, 0.76, title,
                 fontsize=16, fontweight="bold", color=C_ACCENT, ha="center")
        self._ft(fig, 0.5, 0.72,
                 "Automated Environmental Intelligence Report",
                 fontsize=9, color=C_MUTED, ha="center")

        self._hline(fig, 0.67, color=C_ACCENT, lw=1.2)

        # Meta table
        meta = [
            ("Report ID",  report_id),
            ("Generated",  gen_at),
            ("Region(s)",  regions_s),
            ("Template",   report_document.get("templateName",
                           "Full Environmental Assessment")),
            ("Sections",   str(report_document.get("sectionCount",
                               len(sections)))),
        ]
        y = 0.63
        for label, val in meta:
            self._ft(fig, 0.20, y, f"{label}:", fontsize=10,
                     fontweight="bold", color=C_DARK, ha="right")
            self._ft(fig, 0.22, y, val, fontsize=10, color=C_MUTED)
            y -= 0.055

        self._hline(fig, 0.30, color=C_BORDER, lw=0.5)
        self._ft(fig, 0.5, 0.27,
                 "Environmental Decision Support System",
                 fontsize=9, color=C_MUTED, ha="center")
        self._ft(fig, 0.5, 0.24,
                 "Urban Heat Island Mapping & Analytics System — Bangladesh",
                 fontsize=8, color=C_MUTED, ha="center")

        self._draw_footer(fig, report_id, page_num, gen_at)
        all_figs.append(fig)
        page_num += 1

        # ── Region pages ──────────────────────────────────────────────────
        for section in sections:
            region_name = section.get("name", section.get("region", "Unknown"))
            description = section.get("description", "")
            t_stats = section.get("temperatureStatistics") or {}
            n_stats = section.get("ndviStatistics") or {}
            hri     = section.get("heatRiskIndex") or {}
            cli     = section.get("climateScore") or {}
            rec     = section.get("recommendations") or {}

            # ── Build ordered block list ───────────────────────────────────
            # Each block is a callable: fn(fig, y) -> new_y
            blocks = []

            if t_stats:
                t_rows = self._stat_rows(t_stats, [
                    ("mean",   "Mean"),
                    ("max",    "Maximum"),
                    ("min",    "Minimum"),
                    ("median", "Median"),
                    ("std",    "Std. deviation"),
                ])
                t_cf = [0.60, 0.40]
                blocks.append({
                    "h":  _table_h(t_rows, t_cf),
                    "fn": lambda fig, y, _r=t_rows, _cf=t_cf: self._draw_table(
                        fig, y,
                        "Land Surface Temperature (°C)",
                        ["Metric", "Value"], _cf, _r),
                })

            if n_stats:
                n_rows = self._stat_rows(n_stats, [
                    ("mean",   "Mean"),
                    ("max",    "Maximum"),
                    ("min",    "Minimum"),
                    ("median", "Median"),
                    ("std",    "Std. deviation"),
                ], fmt=".4f")
                n_cf = [0.60, 0.40]
                blocks.append({
                    "h":  _table_h(n_rows, n_cf),
                    "fn": lambda fig, y, _r=n_rows, _cf=n_cf: self._draw_table(
                        fig, y,
                        "Normalized Difference Vegetation Index (NDVI)",
                        ["Metric", "Value"], _cf, _r),
                })

            if hri:
                hri_rows = self._stat_rows(hri, [
                    ("average", "Average"),
                    ("max",     "Maximum"),
                    ("min",     "Minimum"),
                ], fmt=".4f")
                h_cf = [0.60, 0.40]
                blocks.append({
                    "h":  _table_h(hri_rows, h_cf),
                    "fn": lambda fig, y, _r=hri_rows, _cf=h_cf: self._draw_table(
                        fig, y, "Heat Risk Index",
                        ["Metric", "Value"], _cf, _r),
                })

                dist = hri.get("riskLevelDistribution") or {}
                d_rows = [[k, str(v)] for k, v in dist.items()]
                if d_rows:
                    d_cf = [0.65, 0.35]
                    blocks.append({
                        "h":  _table_h(d_rows, d_cf),
                        "fn": lambda fig, y, _r=d_rows, _cf=d_cf: self._draw_table(
                            fig, y, "Risk Distribution",
                            ["Category", "Count"], _cf, _r),
                    })

                hotspots = (hri.get("topHotspots") or [])[:5]
                if hotspots:
                    hs_rows = [[
                        f"{h.get('lat', 0):.6f}",
                        f"{h.get('lng', 0):.6f}",
                        f"{h.get('lst', 0):.2f}",
                        f"{h.get('heatRiskIndex', 0):.4f}",
                        str(h.get("riskLevel", "")),
                    ] for h in hotspots]
                    hs_cf = [0.22, 0.22, 0.16, 0.16, 0.24]
                    blocks.append({
                        "h":  _table_h(hs_rows, hs_cf),
                        "fn": lambda fig, y, _r=hs_rows, _cf=hs_cf: self._draw_table(
                            fig, y, "Top Hotspots",
                            ["Latitude", "Longitude", "Temp (°C)", "HRI", "Risk Level"],
                            _cf, _r),
                    })

            if cli:
                c_rows = [
                    ["Resilience Score", f"{cli.get('score', 0):.1f} / 100"],
                    ["Rating",           str(cli.get("category", ""))],
                ]
                c_cf = [0.55, 0.45]
                summary = (cli.get("explanation") or {}).get("summary", "")
                c_extra_lines = textwrap.wrap(summary, 110) if summary else []
                c_extra_h = len(c_extra_lines) * BODY_LEAD + 0.015 if c_extra_lines else 0

                def _draw_climate(fig, y, _r=c_rows, _cf=c_cf,
                                  _sum=summary, _lines=c_extra_lines):
                    y = self._draw_table(fig, y, "Climate Resilience Score",
                                         ["Indicator", "Value"], _cf, _r)
                    if _lines:
                        self._ft(fig, ML, y, "Summary:",
                                 fontsize=FS_BODY, fontweight="bold",
                                 color=C_DARK, va="top")
                        y -= BODY_LEAD
                        for line in _lines:
                            self._ft(fig, ML, y, line, fontsize=FS_BODY,
                                     color=C_MUTED, va="top")
                            y -= BODY_LEAD
                        y -= 0.008
                    return y

                blocks.append({
                    "h":  _table_h(c_rows, c_cf) + c_extra_h,
                    "fn": _draw_climate,
                })

            rec_items = (rec.get("items") or [])[:5]
            if rec_items:
                r_rows = [
                    [
                        str(i.get("locationName", "—")),
                        str(i.get("interventionLevel", "—")),
                        ", ".join(i.get("suggestedActions") or []),
                    ]
                    for i in rec_items
                ]
                r_cf = [0.30, 0.25, 0.45]
                blocks.append({
                    "h":  _table_h(r_rows, r_cf),
                    "fn": lambda fig, y, _r=r_rows, _cf=r_cf: self._draw_table(
                        fig, y, "Green Infrastructure Recommendations",
                        ["Location", "Intervention Level", "Recommended Actions"],
                        _cf, _r),
                })

            # ── Layout blocks across pages ─────────────────────────────────
            fig = self._new_fig()
            y = self._draw_region_heading(fig, TOP_Y, region_name, description)
            first_page = True

            SAFE_BOT = FOOTER_TOP + 0.07   # never render below this

            for block in blocks:
                needed = block["h"]

                if y - needed < SAFE_BOT:
                    # Commit current page
                    self._draw_footer(fig, report_id, page_num, gen_at)
                    all_figs.append(fig)
                    page_num += 1

                    # Start continuation page
                    fig = self._new_fig()
                    y = TOP_Y

                    if not first_page:
                        # Light continuation header
                        self._ft(fig, ML, y,
                                 f"{region_name}  (continued)",
                                 fontsize=10, color=C_MUTED, va="top")
                        y -= 0.030
                        self._hline(fig, y, color=C_BORDER, lw=0.4)
                        y -= 0.015
                    else:
                        first_page = False

                y = block["fn"](fig, y)

            self._draw_footer(fig, report_id, page_num, gen_at)
            all_figs.append(fig)
            page_num += 1

        # ── Render all figures to PDF ──────────────────────────────────────
        with PdfPages(buffer) as pdf:
            for fig in all_figs:
                pdf.savefig(fig, bbox_inches="tight")
                plt.close(fig)

        buffer.seek(0)
        return buffer.getvalue()
