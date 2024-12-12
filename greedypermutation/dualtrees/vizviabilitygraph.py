from ds2viz.styles import *
from ds2viz.default_styles import default_styles
from ds2viz.element import Line, Circle, Group


class VizViabilityGraph(Group):
    def __init__(
        self, viability_graph, style="viability_graph", stylesheet=default_styles
    ):

        super().__init__()
        self.N = viability_graph
        self.stylesheet = stylesheet
        self.style = next(self.stylesheet[style])

        self._vertices("A")
        self._shells()
        self._vertices("B")
        self._viable_edges()
        self._vertex_centers("A")
        self._vertex_centers("B")

    def _viable_edges(self):
        edge_style = self.style.get("viable_edge")
        if edge_style is not None:
            for a in self.N.A:
                for b in self.N.A[a]:
                    self.addelement(
                        Line(a.center, b.center, edge_style, self.stylesheet)
                    )

    def _vertices(self, part):
        if part == "A":
            vertex_style = self.style.get("a_vertex")
            vertices = self.N.A
        else:
            vertex_style = self.style.get("b_vertex")
            vertices = self.N.B
        if vertex_style is not None:
            for vertex in vertices:
                N = Circle(vertex.radius, None, vertex_style, self.stylesheet)
                N.align("center", vertex.center)
                self.addelement(N)

    def _shells(self):
        shell_style = self.style.get("a_shell")
        if shell_style is not None:
            for vertex in self.N.A:
                S = Circle(vertex.radius, None, shell_style, self.stylesheet)
                S.align("center", vertex.center)
                self.addelement(S)

    def _vertex_centers(self, part):
        if part == "A":
            center_style = self.style.get("a_center")
            vertices = self.N.A
        else:
            center_style = self.style.get("b_center")
            vertices = self.N.B
        if center_style is not None:
            center_style_dict = next(self.stylesheet[center_style])
            center_radius = (
                2
                if center_style_dict.get("radius") is None
                else center_style_dict["radius"]
            )
            for vertex in vertices:
                C = Circle(center_radius, None, center_style, self.stylesheet)
                C.align("center", vertex.center)
                self.addelement(C)
