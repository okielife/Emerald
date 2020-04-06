from django.shortcuts import render
from emerald.house_geometry.exterior_walls import wall_vertexes_and_edges, wall_points_only


def index(request):
    return render(
        request,
        'emerald/index.html',
        {"wall_vertex_and_edges": wall_vertexes_and_edges, "wall_points_only": wall_points_only}
    )
