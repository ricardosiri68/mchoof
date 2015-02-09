from PySide.QtCore import QAbstractTableModel


session = get_session()


class TableModel(QAbstractTableModel):
    session = session
    pass
