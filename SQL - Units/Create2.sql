-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `mydb` ;

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Faction`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Faction` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Faction` (
  `id` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`CanTakeAsAllied`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`CanTakeAsAllied` ;

CREATE TABLE IF NOT EXISTS `mydb`.`CanTakeAsAllied` (
  `faction_id` VARCHAR(45) NOT NULL,
  `allied_id` VARCHAR(45) NOT NULL,
  INDEX `fk_allied_Faction_idx` (`faction_id` ASC) INVISIBLE,
  INDEX `fk_allied_Allied_idx` (`allied_id` ASC) VISIBLE,
  CONSTRAINT `fk_allied_Faction`
    FOREIGN KEY (`faction_id`)
    REFERENCES `mydb`.`Faction` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_allied_Faction1`
    FOREIGN KEY (`allied_id`)
    REFERENCES `mydb`.`Faction` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Unit`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Unit` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Unit` (
  `id` VARCHAR(45) NOT NULL,
  `faction_id` VARCHAR(45) NOT NULL,
  `name` VARCHAR(90) NOT NULL,
  `description` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_Unit_Faction1_idx` (`faction_id` ASC) VISIBLE,
  CONSTRAINT `fk_Unit_Faction1`
    FOREIGN KEY (`faction_id`)
    REFERENCES `mydb`.`Faction` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`UnitCost`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`UnitCost` ;

CREATE TABLE IF NOT EXISTS `mydb`.`UnitCost` (
  `unit_id` VARCHAR(45) NOT NULL,
  `model_count` VARCHAR(45) NOT NULL,
  `cost` INT NOT NULL,
  INDEX `fk_UnitCost_Unit1_idx` (`unit_id` ASC) VISIBLE,
  CONSTRAINT `fk_UnitCost_Unit1`
    FOREIGN KEY (`unit_id`)
    REFERENCES `mydb`.`Unit` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Model`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Model` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Model` (
  `id` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `move` VARCHAR(5) NOT NULL,
  `toughness` VARCHAR(5) NOT NULL,
  `wounds` INT NOT NULL,
  `leadership` VARCHAR(3) NOT NULL,
  `save` VARCHAR(3) NOT NULL,
  `unit_id` VARCHAR(45) NOT NULL,
  `oc` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_Model_Unit1_idx` (`unit_id` ASC) VISIBLE,
  CONSTRAINT `fk_Model_Unit1`
    FOREIGN KEY (`unit_id`)
    REFERENCES `mydb`.`Unit` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Weapon`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Weapon` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Weapon` (
  `id` VARCHAR(45) NOT NULL,
  `name` VARCHAR(90) NOT NULL,
  `weapon_range` VARCHAR(10) NOT NULL,
  `strength` VARCHAR(5) NOT NULL,
  `armor_piercing` VARCHAR(10) NOT NULL,
  `damage` VARCHAR(10) NOT NULL,
  `hit_skill` VARCHAR(10) NOT NULL,
  `attack` VARCHAR(10) NOT NULL,
  `unit_id` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Weapon_Unit1_idx` (`unit_id` ASC) VISIBLE,
  CONSTRAINT `fk_Weapon_Unit1`
    FOREIGN KEY (`unit_id`)
    REFERENCES `mydb`.`Unit` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`WeaponKeyword`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`WeaponKeyword` ;

CREATE TABLE IF NOT EXISTS `mydb`.`WeaponKeyword` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(90) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ModelKeyword`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`ModelKeyword` ;

CREATE TABLE IF NOT EXISTS `mydb`.`ModelKeyword` (
  `id` VARCHAR(45) NOT NULL,
  `text` VARCHAR(90) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ModelAbility`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`ModelAbility` ;

CREATE TABLE IF NOT EXISTS `mydb`.`ModelAbility` (
  `id` VARCHAR(45) NOT NULL,
  `description` VARCHAR(1000) NOT NULL,
  `name` VARCHAR(90) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`WeaponHasKeyword`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`WeaponHasKeyword` ;

CREATE TABLE IF NOT EXISTS `mydb`.`WeaponHasKeyword` (
  `Weapon_id` VARCHAR(45) NOT NULL,
  `WeaponKeyword_id` INT NOT NULL,
  INDEX `fk_WeaponHasKeyword_Weapon1_idx` (`Weapon_id` ASC) VISIBLE,
  CONSTRAINT `fk_WeaponHasKeyword_Weapon1`
    FOREIGN KEY (`Weapon_id`)
    REFERENCES `mydb`.`Weapon` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_WeaponHasKeyword_WeaponKeyword1`
    FOREIGN KEY (`WeaponKeyword_id`)
    REFERENCES `mydb`.`WeaponKeyword` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Unit_has_ModelKeyword`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Unit_has_ModelKeyword` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Unit_has_ModelKeyword` (
  `Unit_id` VARCHAR(45) NOT NULL,
  `ModelKeyword_id` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Unit_id`, `ModelKeyword_id`),
  INDEX `fk_Unit_has_ModelKeyword_ModelKeyword1_idx` (`ModelKeyword_id` ASC) VISIBLE,
  INDEX `fk_Unit_has_ModelKeyword_Unit1_idx` (`Unit_id` ASC) VISIBLE,
  CONSTRAINT `fk_Unit_has_ModelKeyword_Unit1`
    FOREIGN KEY (`Unit_id`)
    REFERENCES `mydb`.`Unit` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Unit_has_ModelKeyword_ModelKeyword1`
    FOREIGN KEY (`ModelKeyword_id`)
    REFERENCES `mydb`.`ModelKeyword` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Unit_has_ModelAbility`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Unit_has_ModelAbility` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Unit_has_ModelAbility` (
  `Unit_id` VARCHAR(45) NOT NULL,
  `ModelAbility_id` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Unit_id`, `ModelAbility_id`),
  INDEX `fk_Unit_has_ModelAbility_ModelAbility1_idx` (`ModelAbility_id` ASC) VISIBLE,
  INDEX `fk_Unit_has_ModelAbility_Unit1_idx` (`Unit_id` ASC) VISIBLE,
  CONSTRAINT `fk_Unit_has_ModelAbility_Unit1`
    FOREIGN KEY (`Unit_id`)
    REFERENCES `mydb`.`Unit` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Unit_has_ModelAbility_ModelAbility1`
    FOREIGN KEY (`ModelAbility_id`)
    REFERENCES `mydb`.`ModelAbility` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
