from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.snap import snap_to_grid2x
from gdsfactory.typings import Ints, LayerSpec, Size

valid_port_orientations = {0, 90, 180, -90, 270}


@gf.cell
def compass(
    size: Size = (4.0, 2.0),
    layer: LayerSpec = "WG",
    port_type: str | None = "electrical",
    port_inclusion: float = 0.0,
    port_orientations: Ints | None = (180, 90, 0, -90),
) -> Component:
    """Rectangle with ports on each edge (north, south, east, and west).

    Args:
        size: rectangle size.
        layer: tuple (int, int).
        port_type: optical, electrical.
        port_inclusion: from edge.
        port_orientations: list of port_orientations to add. None does not add ports.
    """
    c = gf.Component()
    dx, dy = snap_to_grid2x(size)
    port_orientations = port_orientations or []

    if dx <= 0 or dy <= 0:
        raise ValueError(f"dx={dx} and dy={dy} must be > 0")

    points = [
        [-dx / 2.0, -dy / 2.0],
        [-dx / 2.0, dy / 2],
        [dx / 2, dy / 2],
        [dx / 2, -dy / 2.0],
    ]

    c.add_polygon(points, layer=layer)

    if port_type:
        for port_orientation in port_orientations:
            if port_orientation not in valid_port_orientations:
                raise ValueError(
                    f"{port_orientation=} must be in {valid_port_orientations}"
                )

        if 180 in port_orientations:
            c.add_port(
                name="e1",
                center=(-dx / 2 + port_inclusion, 0),
                width=dy,
                orientation=180,
                layer=layer,
                port_type=port_type,
            )
        if 90 in port_orientations:
            c.add_port(
                name="e2",
                center=(0, dy / 2 - port_inclusion),
                width=dx,
                orientation=90,
                layer=layer,
                port_type=port_type,
            )
        if 0 in port_orientations:
            c.add_port(
                name="e3",
                center=(dx / 2 - port_inclusion, 0),
                width=dy,
                orientation=0,
                layer=layer,
                port_type=port_type,
            )
        if -90 in port_orientations or 270 in port_orientations:
            c.add_port(
                name="e4",
                center=(0, -dy / 2 + port_inclusion),
                width=dx,
                orientation=-90,
                layer=layer,
                port_type=port_type,
            )

        c.auto_rename_ports()
    return c


if __name__ == "__main__":
    # c = compass(size=(10, 4), port_type="electrical")
    c = compass(port_orientations=[270])
    c.pprint_ports()
    c.show()
