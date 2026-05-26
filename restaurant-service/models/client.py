from dataclasses import dataclass


@dataclass
class Client:
    """Entidad de dominio: representa un cliente del restaurante afiliado."""

    card_number: str
    name: str = ""
    email: str = ""

    def is_new(self) -> bool:
        """Determina si el cliente es nuevo (sin nombre registrado)."""
        return not bool(self.name)
