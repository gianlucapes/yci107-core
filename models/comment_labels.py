from enum import Enum

class CommentLabel(str, Enum):
    Neutrale = "Neutrale"
    Positiva = "Positiva"
    Negativo = "Negativo"
    Discriminatorio = "Discriminatorio"
    Complottismo = "Complottismo"
    Allarmismo = "Allarmismo"
    Disinformazione = "Disinformazione"
    Estremismi_ideologici = "Estremismi ideologici"
