from langchain_core.tools import tool

@tool("booking_appointment", description="Hace el booking de la cita del paciente")
def booking_appointment(fecha: str, tiempo: str, doctor: str, paciente: str) -> str:
    # lógica real: validar, reservar y manejar errores
    return (
        f"Cita confirmada: paciente {paciente}, doctor {doctor}, "
        f"fecha {fecha}, hora {tiempo}."
    )

@tool("get_appointment_availability", description="Valida la disponibilidad del doctor para una cita.")
def get_appointment_availability(fecha: str, tiempo: str, doctor: str) -> str:
    # lógica real: consultar agenda y formatear 'slots' útiles
    return (
        f"Disponibilidad para {doctor} en {fecha} {tiempo}: 14:00, 15:00, 16:00. "
        "Indica tu hora preferida."
    )

tools = [booking_appointment, get_appointment_availability]