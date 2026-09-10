from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle


OUTDIR = Path("outputs")


def add_box(ax, x, y, w, h, fc, ec, lw=1.2, radius=0.016):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.012,rounding_size={radius}",
        facecolor=fc,
        edgecolor=ec,
        linewidth=lw,
    )
    ax.add_patch(patch)
    return patch


def put(ax, x, y, s, size=14, weight="normal", color="#1e3f29", ha="left", va="top", linespacing=1.18):
    ax.text(
        x,
        y,
        s,
        fontsize=size,
        fontweight=weight,
        color=color,
        ha=ha,
        va=va,
        linespacing=linespacing,
        family="DejaVu Sans",
    )


def build_slide(output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(16, 9), dpi=180)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    bg = "#fbf8e8"
    dark = "#173b24"
    green = "#2f7d32"
    olive = "#a7cf63"
    yellow = "#f4d35e"
    pale_yellow = "#fff4bf"
    pale_green = "#dfeecb"
    line = "#bfd09c"
    muted = "#5a6459"

    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)

    ax.add_patch(Rectangle((0, 0.935), 1, 0.065, facecolor=dark, edgecolor="none"))
    put(ax, 0.045, 0.967, "Slide 10 | Ưu tiên hành động", 15, "bold", "#f5ffe3", va="center")

    put(ax, 0.045, 0.885, "Cozy cần làm gì trước?", 31, "bold", dark)
    put(ax, 0.045, 0.836, "Rào cản lớn nhất nằm ở hương vị và khả năng tiếp cận.", 14, "normal", muted)
    put(ax, 0.045, 0.805, "Chiến lược nên đi theo thứ tự: sản phẩm -> điểm bán -> truyền thông -> khuyến mãi.", 14, "normal", muted)

    # Insight strip
    add_box(ax, 0.045, 0.705, 0.91, 0.08, pale_yellow, yellow, lw=1.4)
    put(ax, 0.067, 0.765, "INSIGHT CHÍNH", 11.2, "bold", green)
    put(ax, 0.067, 0.737, "Cozy đã được biết đến khá rộng,", 14.8, "bold", dark)
    put(ax, 0.067, 0.713, "nhưng chưa chuyển hóa tốt thành dùng thường xuyên.", 14.8, "bold", dark)

    # Left panel
    add_box(ax, 0.045, 0.19, 0.54, 0.48, "#ffffff", line, lw=1.4)
    put(ax, 0.065, 0.66, "3 ƯU TIÊN CẦN GIẢI QUYẾT", 11.5, "bold", green)

    priorities = [
        ("P1", "Sửa vị", "Rào cản hương vị: 29,1%", "Làm vị dễ uống hơn, đỡ gắt hơn."),
        ("P1", "Tăng độ sẵn có", "Rào cản availability: 10,0%", "Ưu tiên tủ lạnh, minimart, CVS, văn phòng."),
        ("P2", "Tạo thói quen dùng", "Awareness cao, P4W còn thấp", "Đưa Cozy vào ngữ cảnh sau bữa ăn, giờ nghỉ."),
    ]

    y = 0.50
    for idx, (tag, title, metric, desc) in enumerate(priorities):
        row_y = y - idx * 0.15
        ax.add_patch(Rectangle((0.065, row_y + 0.085), 0.07, 0.025, facecolor=yellow if idx == 0 else olive if idx == 1 else pale_green, edgecolor="none"))
        put(ax, 0.071, row_y + 0.103, tag, 10.4, "bold", dark, va="center")
        put(ax, 0.065, row_y + 0.065, title, 18, "bold", dark)
        put(ax, 0.065, row_y + 0.036, metric, 11.2, "bold", green)
        put(ax, 0.065, row_y + 0.010, desc, 11.2, "normal", muted)
        if idx < 2:
            ax.plot([0.065, 0.55], [row_y - 0.008, row_y - 0.008], color="#e6ead9", lw=1.2)

    # Right top panel
    add_box(ax, 0.62, 0.48, 0.335, 0.2, "#ffffff", line, lw=1.4)
    put(ax, 0.64, 0.655, "THỨ TỰ ƯU TIÊN", 11.5, "bold", green)
    put(ax, 0.64, 0.615, "1. Hương vị: dễ uống hơn, dễ hợp hơn.", 12.4, "bold", dark)
    put(ax, 0.64, 0.57, "2. Độ sẵn có: tăng hiện diện tại điểm mua.", 12.4, "bold", dark)
    put(ax, 0.64, 0.525, "3. Occasion: gắn với thói quen uống hằng ngày.", 12.4, "bold", dark)

    # Right bottom panel
    add_box(ax, 0.62, 0.19, 0.335, 0.24, pale_green, "#8fbb58", lw=1.4)
    put(ax, 0.64, 0.385, "HÀNH ĐỘNG CHỦ ĐẠO", 11.5, "bold", green)
    put(ax, 0.64, 0.345, "Đừng đi thẳng vào giảm giá.", 17, "bold", dark)
    put(ax, 0.64, 0.295, "Hãy làm cho Cozy dễ thích hơn,", 14.2, "bold", dark)
    put(ax, 0.64, 0.267, "dễ tìm hơn, rồi mới dùng khuyến mãi để đẩy thử.", 14.2, "bold", dark)
    put(ax, 0.64, 0.228, "Ưu tiên ngắn gọn: sửa vị -> tăng điểm bán -> tạo occasion -> kích hoạt thử lại.", 11.3, "normal", muted)

    # Footer
    put(ax, 0.045, 0.085, "Thông điệp slide: Cozy không thiếu nhận biết, Cozy thiếu chuyển hóa.", 12.5, "bold", dark)

    fig.savefig(output_path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTDIR / "cozy_action_priority_strategy_slide.png"
    build_slide(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
