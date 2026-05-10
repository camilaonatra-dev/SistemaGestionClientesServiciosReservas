from clases import *

def main():
    clientes = []
    servicios = []
    reservas = []

    print("Iniciando simulación del Sistema de Gestión de Clientes, Servicios y Reservas\n")

    # Operación 1: Registrar cliente válido
    try:
        cliente1 = Cliente(1, "Juan Pérez", "juan@example.com", "123456789")
        clientes.append(cliente1)
        print(f"✓ Cliente registrado: {cliente1}")
    except Exception as e:
        print(f"✗ Error al registrar cliente: {e}")

    # Operación 2: Registrar cliente inválido (email malo)
    try:
        cliente2 = Cliente(2, "Ana Gómez", "ana", "987654321")
        clientes.append(cliente2)
        print(f"✓ Cliente registrado: {cliente2}")
    except InvalidDataError as e:
        print(f"✗ Error al registrar cliente: {e}")
    except Exception as e:
        print(f"✗ Error inesperado: {e}")

    # Operación 3: Crear servicio válido (Reserva de Salas)
    try:
        servicio1 = ReservaSalas(1, "Sala A", 50, 20)
        servicios.append(servicio1)
        print(f"✓ Servicio creado: {servicio1.describir()}")
    except Exception as e:
        print(f"✗ Error al crear servicio: {e}")

    # Operación 4: Crear reserva válida y confirmar
    try:
        reserva1 = Reserva(1, cliente1, servicio1, 2)
        reservas.append(reserva1)
        reserva1.confirmar()
        print(f"✓ Reserva confirmada: {reserva1}")
    except Exception as e:
        print(f"✗ Error al confirmar reserva: {e}")

    # Operación 5: Intentar confirmar reserva con parámetros inválidos
    try:
        reserva2 = Reserva(2, cliente1, servicio1, -1)  # Duración negativa
        reservas.append(reserva2)
        reserva2.confirmar()
        print(f"✓ Reserva confirmada: {reserva2}")
    except (InvalidDataError, ReservationError) as e:
        print(f"✗ Error al confirmar reserva: {e}")
    except Exception as e:
        print(f"✗ Error inesperado: {e}")

    # Operación 6: Cancelar reserva confirmada
    try:
        reserva1.cancelar()
        print(f"✓ Reserva cancelada: {reserva1}")
    except Exception as e:
        print(f"✗ Error al cancelar reserva: {e}")

    # Operación 7: Crear servicio Alquiler de Equipos
    try:
        servicio2 = AlquilerEquipos(2, "Laptop", 30, "Portátil")
        servicios.append(servicio2)
        print(f"✓ Servicio creado: {servicio2.describir()}")
    except Exception as e:
        print(f"✗ Error al crear servicio: {e}")

    # Operación 8: Calcular costo con sobrecarga (descuento)
    try:
        costo = servicio1.calcular_costo(horas=3, descuento=10)
        print(f"✓ Costo calculado con descuento: {costo}")
    except Exception as e:
        print(f"✗ Error al calcular costo: {e}")

    # Operación 9: Crear asesoría y calcular costo con impuesto
    try:
        servicio3 = AsesoriasEspecializadas(3, "Asesoría Python", 100, "Programación")
        servicios.append(servicio3)
        costo = servicio3.calcular_costo(horas=2, nivel_experiencia=3, descuento=5)
        print(f"✓ Costo de asesoría: {costo}")
    except Exception as e:
        print(f"✗ Error al calcular costo: {e}")

    # Operación 10: Intentar reserva con servicio no disponible (capacidad excedida)
    try:
        reserva3 = Reserva(3, cliente1, servicio1, 10)  # Más personas que capacidad, pero en validar no hay personas, ajustar
        # Para simular, modificar validar o crear reserva con personas
        # En ReservaSalas, validar_parametros toma horas, personas, pero en Reserva solo paso duracion.
        # Ajustar: en confirmar, llamar validar_parametros con duracion y 1
        # Para exceder capacidad, crear servicio con capacidad 1 y personas 2, pero no hay personas en Reserva.
        # Simplificar: intentar calcular costo con personas > capacidad
        costo_invalido = servicio1.calcular_costo(horas=1, personas=25)
        print(f"✓ Costo: {costo_invalido}")
    except ServiceUnavailableError as e:
        print(f"✗ Servicio no disponible: {e}")
    except Exception as e:
        print(f"✗ Error: {e}")

    print("\nSimulación completada. El sistema continúa funcionando.")
    print(f"Clientes registrados: {len(clientes)}")
    print(f"Servicios creados: {len(servicios)}")
    print(f"Reservas realizadas: {len(reservas)}")

if __name__ == "__main__":
    main()