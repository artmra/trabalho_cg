# Classe que implementa o que corresponderia ao mundo da nossa aplicação, onde serão armazenados diversos obj 2D
import numpy

from objs import TwoDObj, Line, Wireframe, Point
# from createMenus import CreateTransformMenu
from viewport import Viewport
from window import Window


class World:
    def __init__(self):
        # Lista de objs 2D do mundo
        self.objs = list()
        self.window = Window(self)

    def getWindow(self) -> Window:
        return self.window

    def getObjs(self) -> list:
        # retorna todos os objs
        return self.objs

    def getObj(self, name: str) -> TwoDObj:
        # retorna um obj de attr name equivalente
        try:
            return [obj for obj in self.objs if obj.name == name][0]
        except Exception:
            raise Exception('Não há nenhum objeto com esse nome.')

    def updateObj(self, updatedObj: TwoDObj):
        # como o método de __eq__ dos objetos considera objetos com o mesmo nome iguais é possível atualizar o obj dessa
        # maneira
        self.objs = [updatedObj if updatedObj == obj else obj for obj in self.objs]

    def deleteObj(self, objToDelete: TwoDObj):
        # como o método de __eq__ dos objetos considera objetos com o mesmo nome iguais é possível deletar
        # um abj dessa maneira
        self.objs = [obj for obj in self.objs if obj != objToDelete]

    # translada um obj
    def _translate(self, transformMenu):
        dx = float(transformMenu.desloc_x.text())
        dy = float(transformMenu.desloc_y.text())
        trans_mat = numpy.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])

        transformMenu.trans_matrix = numpy.matmul(transformMenu.trans_matrix, trans_mat)
        transformMenu.logger.appendPlainText(f"-> TRANSLAÇÃO  Eixo X: {dx}    Eixo Y: {dy}\n")

        transformMenu.desloc_x.clear()
        transformMenu.desloc_y.clear()

    # escala um obj
    def _scale(self, transformMenu, current_obj_name: str):
        # current_obj_name = self.objListView.currentText()
        obj = self.getObj(current_obj_name)
        cx, cy = obj.getCenter()

        transformMenu.desloc_x.setText(str(-cx))
        transformMenu.desloc_y.setText(str(-cy))
        self._translate(transformMenu)

        scale_x = float(transformMenu.scale_x.text())
        scale_y = float(transformMenu.scale_y.text())
        scale_mat = numpy.array([[scale_x, 0, 0],
                                 [0, scale_y, 0],
                                 [0, 0, 1]])
        transformMenu.trans_matrix = numpy.matmul(transformMenu.trans_matrix, scale_mat)
        transformMenu.logger.appendPlainText(f"-> ESCALONAMENTO  Eixo X: {scale_x}    Eixo Y: {scale_y}\n")

        transformMenu.desloc_x.setText(str(cx))
        transformMenu.desloc_y.setText(str(cy))
        self._translate(transformMenu)


    # rotaciona um obj em relacao ao mundo
    def click_rotate_world(self, transformMenu, current_obj_name: str):
        self._rotate(around=1, transformMenu=transformMenu, current_obj_name=current_obj_name)

    # rotaciona um obj em relacao ao seu centro
    def click_rotate_obj(self, transformMenu, current_obj_name: str):
        self._rotate(around=2, transformMenu=transformMenu, current_obj_name=current_obj_name)

    # rotaciona um obj em relacao a um ponto
    def click_rotate_point(self, transformMenu, current_obj_name: str):
        self._rotate(around=3, transformMenu=transformMenu, current_obj_name=current_obj_name)

    # rotaciona o obj em relacao a algum referencial
    def _rotate(self, around: int, transformMenu, current_obj_name: str):
        # current_obj_name = self.objListView.currentText()
        obj = self.getObj(current_obj_name)
        dx = 0
        dy = 0

        # rotacionar ao redor do mundo
        if around == 1:
            angle = float(transformMenu.angle1.text())
            transformMenu.logger.appendPlainText(
                f"-> Rotação  de {angle}° em torno do mundo")

        # rotacionar ao redor do centro do obj
        elif around == 2:
            angle = float(transformMenu.angle2.text())
            dx, dy = obj.getCenter()
            transformMenu.logger.appendPlainText(
                f"-> Rotação  de {angle}° em torno do centro do objeto")

        # rotacionar ao redor de um ponto qualquer
        elif around == 3:
            angle = float(transformMenu.angle3.text())
            dx = float(transformMenu.x3.text())
            dy = float(transformMenu.y3.text())
            transformMenu.logger.appendPlainText(
                f"-> Rotação  de {angle}° em torno do ponto ({dx},{dy})")
        # translada para o ponto em torno do qual o obj ira rotacionar
        transformMenu.desloc_x.setText(str(-dx))
        transformMenu.desloc_y.setText(str(-dy))
        self._translate(transformMenu)
        # ROTAÇÃO ACONTECE AQUI
        sin = numpy.sin(angle * numpy.pi / 180)
        # sin = numpy.sin(angle)
        cos = numpy.cos(angle * numpy.pi / 180)
        # cos = numpy.cos(angle)
        rotate_mat = numpy.array([[cos, (-1)*sin, 0],
                                  [sin, cos, 0],
                                  [0, 0, 1]])
        transformMenu.trans_matrix = numpy.matmul(transformMenu.trans_matrix, rotate_mat)
        # translada para o ponto em torno do qual o obj ira rotacionar
        transformMenu.desloc_x.setText(str(dx))
        transformMenu.desloc_y.setText(str(dy))
        self._translate(transformMenu)

    # aplica uma matriz de transformacoes a um obj
    def click_transform(self, transformMenu, current_obj_name: str, viewport: Viewport):
        # pega matriz de transformacoes
        trans_matrix = transformMenu.trans_matrix
        # pega o obj selecionado
        obj = self.getObj(current_obj_name)

        # tratamento para pontos
        if isinstance(obj, Point):
            x = obj.getX()
            y = obj.getY()
            # gera matriz coluna
            x_y = numpy.array([x, y, 1])
            # aplica transformacoes
            new_x, new_y, _ = numpy.matmul(x_y, trans_matrix)
            # atualiza o obj no mundo
            new_obj = Point(obj.name, (new_x, new_y))
            self.updateObj(new_obj)
            # atualiza a viewport
            viewport.update()
            # fecha o menu de transformacoes
            transformMenu.close()

        # tratamento para pontos
        elif isinstance(obj, Line):
            x1 = obj.getX1_Y1()[0]
            y1 = obj.getX1_Y1()[1]
            x2 = obj.getX2_Y2()[0]
            y2 = obj.getX2_Y2()[1]
            # gera as matriz coluna dos pontos do obj
            x_y1 = numpy.array([x1, y1, 1])
            x_y2 = numpy.array([x2, y2, 1])
            # aplica as transformacoes
            new_x1, new_y1, _ = numpy.matmul(x_y1, trans_matrix)
            new_x2, new_y2, _ = numpy.matmul(x_y2, trans_matrix)
            # atualiza o obj no mundo
            new_obj = Line(obj.name, [(new_x1, new_y1), (new_x2, new_y2)])
            self.updateObj(new_obj)
            # atualiza a viewport
            viewport.update()
            # fecha o menu de transformacoes
            transformMenu.close()

        # tratamento para poligonos
        elif isinstance(obj, Wireframe):
            new_coords = list()
            for x_y in obj.getCoords():
                x = x_y[0]
                y = x_y[1]
                # gera matriz para um ponto qualquer
                x_y = numpy.array([x, y, 1])
                # aplica as transformacoes
                new_x, new_y, _ = numpy.matmul(x_y, trans_matrix)
                # adiciona a lista de novas coords do obj
                new_coords.append((new_x, new_y))
            # atualiza o obj no mundo
            new_obj = Wireframe(obj.name, new_coords)
            self.updateObj(new_obj)
            # atualiza a viewport
            viewport.update()
            # fecha o menu de transformacoes
            transformMenu.close()

        # todo: aplicação de transformacoes para window
        else:
            pass
