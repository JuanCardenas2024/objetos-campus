CREATE DATABASE IF NOT EXISTS objetos_campus
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE objetos_campus;

CREATE TABLE IF NOT EXISTS sedes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE,
  departamento VARCHAR(100) NULL
);

CREATE TABLE IF NOT EXISTS usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tipo ENUM('docente', 'estudiante', 'personal') NOT NULL,
  cargo_personal VARCHAR(100) NULL,
  nombre_completo VARCHAR(150) NOT NULL,
  correo_institucional VARCHAR(150) NOT NULL UNIQUE,
  identificacion VARCHAR(30) NOT NULL UNIQUE,
  telefono VARCHAR(20) NOT NULL,
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT chk_cargo_personal
    CHECK (tipo <> 'personal' OR cargo_personal IS NOT NULL)
);

CREATE TABLE IF NOT EXISTS administradores (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario VARCHAR(50) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);