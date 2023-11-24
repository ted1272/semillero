-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-11-2023 a las 02:46:13
-- Versión del servidor: 10.4.27-MariaDB
-- Versión de PHP: 8.0.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `semillero`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `arqueos`
--

CREATE TABLE `arqueos` (
  `idarqueo` double NOT NULL,
  `monto` double NOT NULL,
  `apertura` date NOT NULL,
  `cierre` time DEFAULT NULL,
  `idempleado` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `arqueos`
--

INSERT INTO `arqueos` (`idarqueo`, `monto`, `apertura`, `cierre`, `idempleado`) VALUES
(1, 50000, '2023-11-04', '20:00:00', 1),
(2, 50000, '2023-11-04', '20:00:00', 1),
(3, 50000, '2023-11-05', NULL, 1),
(6, 150000, '2023-11-05', NULL, 1),
(7, 1500000, '2023-11-05', NULL, 1),
(10, 5000, '2023-11-06', NULL, 6),
(11, 1500, '2023-11-07', NULL, 1),
(26, 5000, '2023-11-13', NULL, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrito`
--

CREATE TABLE `carrito` (
  `idcarrito` int(10) NOT NULL,
  `idproducto` int(10) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `hora` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `valor` float NOT NULL,
  `cantidad` int(50) NOT NULL,
  `idempleado` int(15) NOT NULL,
  `empleado` varchar(100) NOT NULL,
  `idaqueo` int(12) NOT NULL,
  `idcliente` int(12) NOT NULL,
  `nombrecliente` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `idcliente` int(11) NOT NULL,
  `nombrecliente` varchar(100) NOT NULL,
  `telefono` varchar(100) NOT NULL,
  `direccion` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`idcliente`, `nombrecliente`, `telefono`, `direccion`) VALUES
(5, 'jorge', '3102513062', 'calle 57 #9-20'),
(7, 'daniel', '123454', 'calle 90');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleados`
--

CREATE TABLE `empleados` (
  `idempleado` double NOT NULL,
  `nombreempleado` varchar(250) NOT NULL,
  `cargo` varchar(250) NOT NULL,
  `correo` varchar(250) NOT NULL,
  `usuario` varchar(250) NOT NULL,
  `clave` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `empleados`
--

INSERT INTO `empleados` (`idempleado`, `nombreempleado`, `cargo`, `correo`, `usuario`, `clave`) VALUES
(1, 'Jorg Ramos', 'administrador', 'ramos014@hotmail.com', 'admin', 'jorge123'),
(5, 'miguel', 'cajero', 'miguel@hotmail.com', 'ted', '123'),
(6, 'Daniel', 'mesero', 'daniel@', 'cajero', '123');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gastos`
--

CREATE TABLE `gastos` (
  `idgastos` int(11) NOT NULL,
  `factura` varchar(150) NOT NULL,
  `valor` double NOT NULL,
  `nombreproveedor` varchar(150) NOT NULL,
  `pago` varchar(150) NOT NULL,
  `idproveedores` int(11) NOT NULL,
  `idarqueo` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `idproducto` int(11) NOT NULL,
  `nombreproducto` varchar(100) NOT NULL,
  `precio` double NOT NULL,
  `codigo` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `idproveedores` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`idproducto`, `nombreproducto`, `precio`, `codigo`, `cantidad`, `idproveedores`) VALUES
(7, 'grafica', 1500000, 50, 0, 1),
(8, 'llanta', 110000, 5, 11, 1),
(9, 'llanta', 110000, 5, 5, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `idproveedores` int(11) NOT NULL,
  `nombrepro` varchar(100) NOT NULL,
  `nit` varchar(150) NOT NULL,
  `direccion` varchar(150) NOT NULL,
  `telefono` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proveedores`
--

INSERT INTO `proveedores` (`idproveedores`, `nombrepro`, `nit`, `direccion`, `telefono`) VALUES
(1, 'losalpes', '789456', 'calle 80', 123456),
(3, 'corona', '123456', 'calle80', 7894564);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `idventa` int(11) NOT NULL,
  `pago` varchar(100) DEFAULT NULL,
  `valor` float NOT NULL,
  `horainicial` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `horafinal` datetime NOT NULL,
  `idproducto` int(11) NOT NULL,
  `idempleado` double NOT NULL,
  `idarqueo` double NOT NULL,
  `idcliente` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ventas`
--

INSERT INTO `ventas` (`idventa`, `pago`, `valor`, `horainicial`, `horafinal`, `idproducto`, `idempleado`, `idarqueo`, `idcliente`) VALUES
(1, 'nequi', 5000, '2023-11-06 01:55:45', '2023-11-06 04:55:45', 7, 5, 1, 7),
(2, NULL, 1500000, '2023-11-14 05:33:00', '2023-11-15 18:11:09', 7, 5, 26, 7),
(3, NULL, 110000, '2023-11-15 22:04:02', '2023-11-15 18:11:09', 8, 5, 26, 7),
(4, NULL, 110000, '2023-11-15 22:19:41', '2023-11-15 18:11:09', 9, 5, 26, 7),
(5, NULL, 1500000, '2023-11-14 05:33:00', '2023-11-15 18:15:06', 7, 5, 26, 7),
(6, NULL, 110000, '2023-11-15 22:04:02', '2023-11-15 18:15:06', 8, 5, 26, 7),
(7, NULL, 110000, '2023-11-15 22:19:41', '2023-11-15 18:15:06', 9, 5, 26, 7),
(8, NULL, 1500000, '2023-11-14 05:33:00', '2023-11-15 18:15:31', 7, 5, 26, 7),
(9, NULL, 110000, '2023-11-15 22:04:02', '2023-11-15 18:15:31', 8, 5, 26, 7),
(10, NULL, 110000, '2023-11-15 22:19:41', '2023-11-15 18:15:31', 9, 5, 26, 7),
(11, 'credito', 1500000, '2023-11-14 05:33:00', '2023-11-15 18:20:47', 7, 5, 26, 7),
(12, 'credito', 110000, '2023-11-15 22:04:02', '2023-11-15 18:20:47', 8, 5, 26, 7),
(13, 'credito', 110000, '2023-11-15 22:19:41', '2023-11-15 18:20:47', 9, 5, 26, 7),
(14, 'daviplata', 1500000, '2023-11-14 01:17:09', '2023-11-15 18:21:00', 7, 5, 26, 5),
(15, 'daviplata', 1500000, '2023-11-14 01:17:09', '2023-11-15 18:21:00', 7, 5, 26, 5),
(16, 'daviplata', 1500000, '2023-11-14 01:17:09', '2023-11-15 18:21:00', 7, 5, 26, 5),
(17, 'daviplata', 1500000, '2023-11-14 01:17:10', '2023-11-15 18:21:00', 7, 5, 26, 5),
(20, 'credito', 1500000, '2023-11-14 05:33:00', '2023-11-15 18:32:39', 7, 5, 26, 7),
(21, 'credito', 110000, '2023-11-15 23:26:50', '2023-11-15 18:32:39', 8, 5, 26, 7),
(22, 'efectivo', 1500000, '2023-11-14 05:33:00', '2023-11-15 18:33:18', 7, 5, 26, 7),
(23, 'credito', 7500000, '2023-11-15 23:33:33', '2023-11-15 18:33:58', 7, 5, 26, 7),
(24, 'credito', 550000, '2023-11-15 23:33:45', '2023-11-15 18:33:58', 8, 5, 26, 7),
(25, 'daviplata', 3000000, '2023-11-15 23:38:55', '2023-11-15 18:39:01', 7, 5, 26, 5),
(26, 'efectivo', 4500000, '2023-11-15 23:42:21', '2023-11-15 18:42:29', 7, 5, 26, 5),
(27, 'credito', 3000000, '2023-11-15 23:44:34', '2023-11-15 18:44:39', 7, 5, 26, 5),
(28, 'efectivo', 3000000, '2023-11-15 23:44:54', '2023-11-15 18:44:57', 7, 5, 26, 5),
(29, 'nequi', 1500000, '2023-11-15 23:45:33', '2023-11-15 18:45:36', 7, 5, 26, 5),
(30, 'daviplata', 330000, '2023-11-16 01:42:43', '2023-11-15 20:43:38', 8, 5, 26, 7);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `arqueos`
--
ALTER TABLE `arqueos`
  ADD PRIMARY KEY (`idarqueo`),
  ADD KEY `idempleado` (`idempleado`);

--
-- Indices de la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD PRIMARY KEY (`idcarrito`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`idcliente`);

--
-- Indices de la tabla `empleados`
--
ALTER TABLE `empleados`
  ADD PRIMARY KEY (`idempleado`);

--
-- Indices de la tabla `gastos`
--
ALTER TABLE `gastos`
  ADD PRIMARY KEY (`idgastos`),
  ADD KEY `idproveedores` (`idproveedores`,`idarqueo`),
  ADD KEY `idarqueo` (`idarqueo`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`idproducto`),
  ADD KEY `idproveedores` (`idproveedores`);

--
-- Indices de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`idproveedores`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`idventa`),
  ADD KEY `idproducto` (`idproducto`,`idempleado`,`idarqueo`,`idcliente`),
  ADD KEY `idempleado` (`idempleado`),
  ADD KEY `idarqueo` (`idarqueo`),
  ADD KEY `idcliente` (`idcliente`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `arqueos`
--
ALTER TABLE `arqueos`
  MODIFY `idarqueo` double NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT de la tabla `carrito`
--
ALTER TABLE `carrito`
  MODIFY `idcarrito` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=90;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `idcliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `empleados`
--
ALTER TABLE `empleados`
  MODIFY `idempleado` double NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `gastos`
--
ALTER TABLE `gastos`
  MODIFY `idgastos` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `idproducto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  MODIFY `idproveedores` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `idventa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `arqueos`
--
ALTER TABLE `arqueos`
  ADD CONSTRAINT `arqueos_ibfk_1` FOREIGN KEY (`idempleado`) REFERENCES `empleados` (`idempleado`);

--
-- Filtros para la tabla `gastos`
--
ALTER TABLE `gastos`
  ADD CONSTRAINT `gastos_ibfk_1` FOREIGN KEY (`idproveedores`) REFERENCES `proveedores` (`idproveedores`),
  ADD CONSTRAINT `gastos_ibfk_2` FOREIGN KEY (`idarqueo`) REFERENCES `arqueos` (`idarqueo`);

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`idproveedores`) REFERENCES `proveedores` (`idproveedores`);

--
-- Filtros para la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`idempleado`) REFERENCES `empleados` (`idempleado`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `ventas_ibfk_2` FOREIGN KEY (`idarqueo`) REFERENCES `arqueos` (`idarqueo`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `ventas_ibfk_3` FOREIGN KEY (`idcliente`) REFERENCES `clientes` (`idcliente`),
  ADD CONSTRAINT `ventas_ibfk_4` FOREIGN KEY (`idproducto`) REFERENCES `productos` (`idproducto`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
