-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 25, 2022 at 10:28 AM
-- Server version: 10.4.19-MariaDB
-- PHP Version: 7.4.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `efarmer`
--

-- --------------------------------------------------------

--
-- Table structure for table `diseases_and_treatments`
--

CREATE TABLE `diseases_and_treatments` (
  `id` int(255) NOT NULL,
  `plant_name` varchar(255) NOT NULL,
  `disease_name` varchar(255) NOT NULL,
  `details` varchar(500) NOT NULL,
  `treatments` varchar(500) NOT NULL,
  `image` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `diseases_and_treatments`
--

INSERT INTO `diseases_and_treatments` (`id`, `plant_name`, `disease_name`, `details`, `treatments`, `image`) VALUES
(7, 'Potato ', 'Common Scab (Streptomyces spp.) ', 'Common scab produces tan to dark brown, circular or irregular lesions which are rough in texture. Scab may be superficial (russet scab), slightly raised (erumpent scab), or sunken (pitted \r\n\r\nscab). The type of lesion is dependent on potato cultivar, tuber maturity at infection, organic matter content of soil, strain of the pathogen, and the environment. Common scab is controlled or greatly suppressed at soil pH levels of 5.2 or lower, though a closely related but less common species of Streptom', 'A shallow or surface scab is a superficial, roughened or russeted area on the tuber. Slight protuberances with depressed centres might form and are covered with a small amount of corky tissue.', 'Potato _Common Scab (Streptomyces spp.) _scab_rw_samson.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `system_users`
--

CREATE TABLE `system_users` (
  `id` int(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `psw` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `system_users`
--

INSERT INTO `system_users` (`id`, `name`, `email`, `psw`) VALUES
(1, 'Maleesha', 'maleesha@gmail.com', '25d55ad283aa400af464c76d713c07ad'),
(3, 'Nirmal', 'nirmal@gmail.com', '25d55ad283aa400af464c76d713c07ad');

-- --------------------------------------------------------

--
-- Table structure for table `trained_classes`
--

CREATE TABLE `trained_classes` (
  `id` int(255) NOT NULL,
  `disease_name` varchar(255) NOT NULL,
  `plant_name` varchar(255) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `diseases_and_treatments`
--
ALTER TABLE `diseases_and_treatments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `system_users`
--
ALTER TABLE `system_users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `trained_classes`
--
ALTER TABLE `trained_classes`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `diseases_and_treatments`
--
ALTER TABLE `diseases_and_treatments`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `system_users`
--
ALTER TABLE `system_users`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `trained_classes`
--
ALTER TABLE `trained_classes`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
