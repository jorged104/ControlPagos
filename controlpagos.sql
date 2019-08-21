-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 21-08-2019 a las 03:10:48
-- Versión del servidor: 10.3.16-MariaDB
-- Versión de PHP: 7.1.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `controlpagos`
--

DELIMITER $$
--
-- Procedimientos
--
DROP PROCEDURE IF EXISTS `ingreso_cobro`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `ingreso_cobro` (IN `id` INT, IN `valor` DECIMAL(10,2))  BEGIN 
	DECLARE saldo_actual DECIMAL(10,2);
	DECLARE saldo_nuevo  DECIMAL(10,2); 
	
    SELECT `SALDO` INTO saldo_actual FROM cliente WHERE cliente.idCliente = id ;
	
	SET saldo_nuevo = saldo_actual + valor ; 
	
	UPDATE  cliente SET saldo = saldo_nuevo WHERE idCliente = id ;  
	
    SELECT saldo_nuevo;
    COMMIT;
END$$

DROP PROCEDURE IF EXISTS `ingreso_pago`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `ingreso_pago` (IN `id` INT, IN `valor` DECIMAL(10,2))  BEGIN 
	DECLARE saldo_actual DECIMAL(10,2);
	DECLARE saldo_nuevo  DECIMAL(10,2); 
	SELECT `SALDO` INTO saldo_actual FROM cliente WHERE cliente.idCliente = id ;
	
	SET saldo_nuevo = saldo_actual - valor ; 
	
	UPDATE  cliente SET SALDO = saldo_nuevo WHERE idCliente = id ;  
	COMMIT;
END$$

DROP PROCEDURE IF EXISTS `setCobro`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `setCobro` (IN `c` INT, IN `idc` INT)  NO SQL
BEGIN 	
	UPDATE  cobros SET idpago = idc WHERE idcobro = c ;  
    COMMIT;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

DROP TABLE IF EXISTS `cliente`;
CREATE TABLE `cliente` (
  `idCliente` int(11) NOT NULL,
  `NIT` int(11) NOT NULL,
  `NOMBRE` text COLLATE latin1_spanish_ci NOT NULL,
  `MENSUAL` decimal(10,2) NOT NULL,
  `DIRECCION` text COLLATE latin1_spanish_ci NOT NULL,
  `TELEFONO` varchar(15) COLLATE latin1_spanish_ci NOT NULL,
  `EMAIL` varchar(255) COLLATE latin1_spanish_ci NOT NULL,
  `REGIMEN` text COLLATE latin1_spanish_ci NOT NULL,
  `SALDO` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cobros`
--

DROP TABLE IF EXISTS `cobros`;
CREATE TABLE `cobros` (
  `idcobro` int(11) NOT NULL,
  `fechaCobro` date NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `idusuario` int(11) NOT NULL,
  `idpago` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pago`
--

DROP TABLE IF EXISTS `pago`;
CREATE TABLE `pago` (
  `idPago` int(11) NOT NULL,
  `idCliente` int(11) NOT NULL,
  `fechaPago` date NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `descripcion` text COLLATE latin1_spanish_ci DEFAULT NULL,
  `tipo` varchar(255) COLLATE latin1_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`idCliente`);

--
-- Indices de la tabla `cobros`
--
ALTER TABLE `cobros`
  ADD PRIMARY KEY (`idcobro`),
  ADD KEY `idusuario` (`idusuario`),
  ADD KEY `idpago` (`idpago`);

--
-- Indices de la tabla `pago`
--
ALTER TABLE `pago`
  ADD PRIMARY KEY (`idPago`),
  ADD KEY `idCliente` (`idCliente`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `idCliente` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cobros`
--
ALTER TABLE `cobros`
  MODIFY `idcobro` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pago`
--
ALTER TABLE `pago`
  MODIFY `idPago` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `cobros`
--
ALTER TABLE `cobros`
  ADD CONSTRAINT `cobros_ibfk_1` FOREIGN KEY (`idusuario`) REFERENCES `cliente` (`idCliente`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `cobros_ibfk_2` FOREIGN KEY (`idpago`) REFERENCES `pago` (`idPago`) ON DELETE SET NULL ON UPDATE NO ACTION;

--
-- Filtros para la tabla `pago`
--
ALTER TABLE `pago`
  ADD CONSTRAINT `pago_ibfk_1` FOREIGN KEY (`idCliente`) REFERENCES `cliente` (`idCliente`) ON DELETE CASCADE ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
