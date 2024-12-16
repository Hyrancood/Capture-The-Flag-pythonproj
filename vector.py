"""Двумерный вектор"""
class Vector():
    """
    Двумерный вектор

    :ivar x: значение по 'x'-кординате
    :type x: int|float
    :ivar y: значение по 'y'-кординате
    :type y: int|float
    """
    def __init__(self, x: int|float = 0, y: int|float = 0):
        """
        Создание нового экземпляра

        :param x: длина вектора по 'x'-кординате
        :param y: длина вектора по 'y'-кординате
        """
        self.x = x
        self.y = y

    def set(self, x, y):
        """
        Переопределяет вектор

        :param x: новое значение по 'x'
        :param y: новое значение по 'y'
        """
        self.x = x
        self.y = y

