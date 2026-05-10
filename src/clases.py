import abc
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(filename='../logs.txt', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Excepciones personalizadas
class InvalidDataError(Exception):
    pass

class ServiceUnavailableError(Exception):
    pass

class ReservationError(Exception):
    pass

class CalculationError(Exception):
    pass

# Clase abstracta Entidad
class Entidad(abc.ABC):
    def __init__(self, id_entidad):
        self._id = id_entidad

    @property
    def id(self):
        return self._id

    @abc.abstractmethod
    def validar(self):
        pass

# Clase Cliente
class Cliente(Entidad):
    def __init__(self, id_cliente, nombre, email, telefono):
        super().__init__(id_cliente)
        self._nombre = nombre
        self._email = email
        self._telefono = telefono
        self.validar()

    @property
    def nombre(self):
        return self._nombre

    @property
    def email(self):
        return self._email

    @property
    def telefono(self):
        return self._telefono

    def validar(self):
        if not self._nombre or len(self._nombre.strip()) < 2:
            raise InvalidDataError("Nombre inválido")
        if not self._email or '@' not in self._email:
            raise InvalidDataError("Email inválido")
        if not self._telefono or len(self._telefono) < 7:
            raise InvalidDataError("Teléfono inválido")

    def __str__(self):
        return f"Cliente {self._id}: {self._nombre}"

# Clase abstracta Servicio
class Servicio(abc.ABC):
    def __init__(self, id_servicio, nombre, costo_base):
        self._id = id_servicio
        self._nombre = nombre
        self._costo_base = costo_base

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @abc.abstractmethod
    def calcular_costo(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def describir(self):
        pass

    @abc.abstractmethod
    def validar_parametros(self, *args, **kwargs):
        pass

# Servicio: Reserva de Salas
class ReservaSalas(Servicio):
    def __init__(self, id_servicio, nombre, costo_base, capacidad_maxima):
        super().__init__(id_servicio, nombre, costo_base)
        self._capacidad_maxima = capacidad_maxima

    def calcular_costo(self, horas=1, personas=1, descuento=0):
        try:
            if personas > self._capacidad_maxima:
                raise ServiceUnavailableError("Capacidad excedida")
            costo = self._costo_base * horas * (1 - descuento / 100)
            return costo
        except Exception as e:
            logging.error(f"Error en calcular_costo ReservaSalas: {e}")
            raise CalculationError("Error en cálculo de costo")

    def describir(self):
        return f"Reserva de sala: {self._nombre}, capacidad {self._capacidad_maxima}"

    def validar_parametros(self, horas, personas):
        if horas <= 0 or personas <= 0:
            raise InvalidDataError("Parámetros inválidos para reserva de sala")

# Servicio: Alquiler de Equipos
class AlquilerEquipos(Servicio):
    def __init__(self, id_servicio, nombre, costo_base, tipo_equipo):
        super().__init__(id_servicio, nombre, costo_base)
        self._tipo_equipo = tipo_equipo

    def calcular_costo(self, dias=1, cantidad=1, impuesto=0):
        try:
            costo = self._costo_base * dias * cantidad * (1 + impuesto / 100)
            return costo
        except Exception as e:
            logging.error(f"Error en calcular_costo AlquilerEquipos: {e}")
            raise CalculationError("Error en cálculo de costo")

    def describir(self):
        return f"Alquiler de equipo: {self._nombre}, tipo {self._tipo_equipo}"

    def validar_parametros(self, dias, cantidad):
        if dias <= 0 or cantidad <= 0:
            raise InvalidDataError("Parámetros inválidos para alquiler de equipos")

# Servicio: Asesorías Especializadas
class AsesoriasEspecializadas(Servicio):
    def __init__(self, id_servicio, nombre, costo_base, especialidad):
        super().__init__(id_servicio, nombre, costo_base)
        self._especialidad = especialidad

    def calcular_costo(self, horas=1, nivel_experiencia=1, descuento=0):
        try:
            costo = self._costo_base * horas * nivel_experiencia * (1 - descuento / 100)
            return costo
        except Exception as e:
            logging.error(f"Error en calcular_costo AsesoriasEspecializadas: {e}")
            raise CalculationError("Error en cálculo de costo")

    def describir(self):
        return f"Asesoría especializada: {self._nombre}, especialidad {self._especialidad}"

    def validar_parametros(self, horas, nivel_experiencia):
        if horas <= 0 or nivel_experiencia < 1 or nivel_experiencia > 5:
            raise InvalidDataError("Parámetros inválidos para asesoría")

# Clase Reserva
class Reserva:
    def __init__(self, id_reserva, cliente, servicio, duracion):
        self._id = id_reserva
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "Pendiente"
        self._costo_total = 0

    @property
    def id(self):
        return self._id

    @property
    def estado(self):
        return self._estado

    def confirmar(self):
        try:
            self._servicio.validar_parametros(self._duracion, 1)  # Simplificado
            self._costo_total = self._servicio.calcular_costo(self._duracion)
            self._estado = "Confirmada"
        except Exception as e:
            logging.error(f"Error al confirmar reserva {self._id}: {e}")
            raise ReservationError("No se pudo confirmar la reserva")

    def cancelar(self):
        if self._estado == "Confirmada":
            self._estado = "Cancelada"
        else:
            raise ReservationError("No se puede cancelar una reserva no confirmada")

    def __str__(self):
        return f"Reserva {self._id}: {self._cliente.nombre} - {self._servicio.nombre} - Estado: {self._estado}"