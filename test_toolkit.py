import pytest
from log_parser import analizar_logs
from os_utils import check_ping

def test_contar_ips():
    lineas_prueba = [
        "May 19 08:23:11 server sshd[1234]: Failed password for root from 192.168.1.100 port 22 ssh2",
        "May 19 08:23:15 server sshd[1234]: Failed password for root from 192.168.1.100 port 22 ssh2",
        "May 19 08:23:18 server sshd[1234]: Failed password for admin from 45.33.32.156 port 22 ssh2",
    ]
    
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False) as f:
        f.writelines(linea + "\n" for linea in lineas_prueba)
        archivo_temp = f.name
    
    resultado = analizar_logs(archivo_temp)
    os.unlink(archivo_temp)
    
    assert resultado["192.168.1.100"] == 2
    assert resultado["45.33.32.156"] == 1

def test_archivo_inexistente():
    resultado = analizar_logs("archivo_que_no_existe.log")
    assert resultado == {}

def test_ping_ip_invalida():
    resultado = check_ping("0.0.0.0")
    assert resultado == False