# Programación Orientada a Objetos en Redes

## ¿Por qué usar POO para gestionar un inventario de red?

Un administrador de sistemas gestiona distintos tipos de dispositivos:
routers, servidores, switches, firewalls. Cada uno tiene características
comunes pero también propiedades y comportamientos específicos.

Sin POO tendríamos funciones sueltas y diccionarios mezclados, difíciles
de mantener. Con POO modelamos la red igual que existe en la realidad.

## Estructura de clases
NetworkDevice (clase base)
├── hostname
├── ip
├── mac
└── audit_device()
├── Router (clase hija)
│   ├── modelo
│   └── audit_device() → directrices de router
└── Server (clase hija)
├── os
└── audit_device() → directrices de servidor

## Conceptos aplicados

**Herencia** — `Router` y `Server` heredan de `NetworkDevice`. No
repetimos el código de hostname, IP y MAC en cada clase.

**Polimorfismo** — los tres tienen `audit_device()` pero cada uno
hace algo diferente. Podemos recorrer una lista mixta de dispositivos
y cada uno sabe qué auditoría mostrar.

**Encapsulación** — cada clase gestiona sus propios datos y métodos.
El resto del código no necesita saber cómo funciona internamente.

## Ejemplo práctico

```python
dispositivos = [
    Router("router-01", "192.168.1.1", "AA:BB:CC", "Cisco"),
    Server("servidor-web", "192.168.1.10", "DD:EE:FF", "Ubuntu"),
    Server("servidor-bd", "192.168.1.11", "GG:HH:II", "Windows"),
]

for dispositivo in dispositivos:
    dispositivo.audit_device()
```

Con este código auditamos automáticamente toda la red — cada dispositivo
aplica sus propias directrices de seguridad sin necesidad de comprobar
manualmente qué tipo es.

## Ventajas para el administrador de sistemas

- **Escalabilidad** — añadir un nuevo tipo de dispositivo es crear
  una nueva clase hija, sin tocar el código existente.
- **Mantenibilidad** — si cambian las directrices de seguridad de los
  routers, solo se modifica la clase `Router`.
- **Legibilidad** — el código refleja la estructura real de la red.
