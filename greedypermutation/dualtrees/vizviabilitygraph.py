from ds2viz.styles import *
from ds2viz.default_styles import default_styles
from ds2viz.element import Line, Circle, Group


class VizViabilityGraph(Group):
    def __init__(
        self, viability_graph, style="viability_graph", stylesheet=default_styles
    ):

        super().__init__()
        self.N = viability_graph
        # self.A = self.B = []
        self.stylesheet = stylesheet
        self.style = next(self.stylesheet[style])

        self._viable_edges()
        self._vertices('A')
        self._vertices('B')


    # def _points(self, part):
    #     if part == 'A':
    #         point_style = self.style.get("a_point")
    #         points = self.A
    #     else:
    #         point_style = self.style.get("b_point")
    #         points = self.B
    #     if point_style is not None:
    #         point_style_dict = next(self.stylesheet[point_style])
    #         point_radius = (
    #             1
    #             if point_style_dict.get("radius") is None
    #             else point_style_dict["radius"]
    #         )
    #         for p in points:
    #             C = Circle(point_radius, None, point_style, self.stylesheet)
    #             C.align("center", p)
    #             self.addelement(C)

    def _viable_edges(self):
        edge_style = self.style.get("viable_edge")
        if edge_style is not None:
            for a in self.N.A:
                for b in self.N.A[a]:
                    self.addelement(Line(a.center, b.center, edge_style, self.stylesheet))


    def _vertices(self, part):
        if part == 'A':
            vertex_style = self.style.get("a_vertex")
            center_style = self.style.get("a_center")
            vertices = self.N.A
        else:
            vertex_style = self.style.get("b_vertex")
            center_style = self.style.get("b_center")
            vertices = self.N.B
        if vertex_style is not None:
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
                N = Circle(vertex.radius, None, vertex_style, self.stylesheet)
                N.align("center", vertex.center)
                self.addelement(N)
        

    # def _points(self):
    #     point_style = self.style.get("graph_point")
    #     node_style = self.style.get("graph_node")
    #     if point_style is not None:
    #         point_style_dict = next(self.stylesheet[point_style])
    #         point_radius = (
    #             2
    #             if point_style_dict.get("radius") is None
    #             else point_style_dict["radius"]
    #         )
    #         for cell in self.N.vertices():
    #             for point in cell.points:
    #                 C = Circle(point_radius, None, point_style, self.stylesheet)
    #                 C.align("center", point.center)
    #                 self.addelement(C)
    #                 N = Circle(point.radius, None, node_style, self.stylesheet)
    #                 N.align("center", point.center)
    #                 self.addelement(N)
    #                 # canvas.circle(point, 2,  point_style)
    #             # canvas.circle(vertex.center, 2, point_style)
