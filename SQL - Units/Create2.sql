-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Faction`
-- -----------------------------------------------------
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
CREATE TABLE IF NOT EXISTS `mydb`.`Unit` (
  `id` VARCHAR(45) NOT NULL,
  `faction_id` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
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
CREATE TABLE IF NOT EXISTS `mydb`.`UnitCost` (
  `unit_id` INT NOT NULL,
  `model_count` INT NOT NULL,
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
CREATE TABLE IF NOT EXISTS `mydb`.`Model` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `move` INT NOT NULL,
  `wound_save` INT NOT NULL,
  `strength` INT NOT NULL,
  `toughness` INT NOT NULL,
  `wounds` INT NOT NULL,
  `attacks` INT NOT NULL,
  `leadership` INT NOT NULL,
  `save` INT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`UnitCanContainModel`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`UnitCanContainModel` (
  `unit_id` VARCHAR(45) NOT NULL,
  `model_id` VARCHAR(45) NOT NULL,
  INDEX `fk_UnitCanContain_Unit1_idx` (`unit_id` ASC) VISIBLE,
  INDEX `fk_UnitCanContain_Model1_idx` (`model_id` ASC) VISIBLE,
  CONSTRAINT `fk_UnitCanContain_Unit1`
    FOREIGN KEY (`unit_id`)
    REFERENCES `mydb`.`Unit` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_UnitCanContain_Model1`
    FOREIGN KEY (`model_id`)
    REFERENCES `mydb`.`Model` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Weapon`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Weapon` (
  `id` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `range` INT NOT NULL,
  `strength` INT NOT NULL,
  `armor_piercing` INT NOT NULL,
  `damage` INT NOT NULL,
  `balistic_skill` INT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ModelCanUseWeapon`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ModelCanUseWeapon` (
  `model_id` VARCHAR(45) NOT NULL,
  `weapon_id` VARCHAR(45) NOT NULL,
  INDEX `fk_ModelCanUse_Model1_idx` (`model_id` ASC) VISIBLE,
  INDEX `fk_ModelCanUse_Weapon1_idx` (`weapon_id` ASC) VISIBLE,
  CONSTRAINT `fk_ModelCanUse_Model1`
    FOREIGN KEY (`model_id`)
    REFERENCES `mydb`.`Model` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ModelCanUse_Weapon1`
    FOREIGN KEY (`weapon_id`)
    REFERENCES `mydb`.`Weapon` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`WeaponKeyword`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`WeaponKeyword` (
  `id` VARCHAR(45) NOT NULL,
  `text` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`SpecialRules`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`SpecialRules` (
  `unit_id` VARCHAR(45) NOT NULL,
  `rule` VARCHAR(45) NOT NULL,
  INDEX `fk_SpecialRules_Unit1_idx` (`unit_id` ASC) VISIBLE,
  CONSTRAINT `fk_SpecialRules_Unit1`
    FOREIGN KEY (`unit_id`)
    REFERENCES `mydb`.`Unit` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ModelKeyword`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ModelKeyword` (
  `id` VARCHAR(45) NOT NULL,
  `text` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`WeaponAbility`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`WeaponAbility` (
  `id` VARCHAR(45) NOT NULL,
  `text` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ModelAbility`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ModelAbility` (
  `id` VARCHAR(45) NOT NULL,
  `text` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ModelHasAbility`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ModelHasAbility` (
  `model_id` VARCHAR(45) NOT NULL,
  `modelAbility_id` VARCHAR(45) NOT NULL,
  INDEX `fk_ModelHasAbility_Model1_idx` (`model_id` ASC) VISIBLE,
  INDEX `fk_ModelHasAbility_ModelAbility1_idx` (`modelAbility_id` ASC) VISIBLE,
  CONSTRAINT `fk_ModelHasAbility_Model1`
    FOREIGN KEY (`model_id`)
    REFERENCES `mydb`.`Model` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ModelHasAbility_ModelAbility1`
    FOREIGN KEY (`modelAbility_id`)
    REFERENCES `mydb`.`ModelAbility` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ModelHasKeyword`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ModelHasKeyword` (
  `Model_id` VARCHAR(45) NOT NULL,
  `ModelKeyword_id` VARCHAR(45) NOT NULL,
  INDEX `fk_ModelHasKeyword_Model1_idx` (`Model_id` ASC) VISIBLE,
  INDEX `fk_ModelHasKeyword_ModelKeyword1_idx` (`ModelKeyword_id` ASC) VISIBLE,
  CONSTRAINT `fk_ModelHasKeyword_Model1`
    FOREIGN KEY (`Model_id`)
    REFERENCES `mydb`.`Model` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ModelHasKeyword_ModelKeyword1`
    FOREIGN KEY (`ModelKeyword_id`)
    REFERENCES `mydb`.`ModelKeyword` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`WeaponHasKeyword`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`WeaponHasKeyword` (
  `Weapon_id` VARCHAR(45) NOT NULL,
  `WeaponKeyword_id` VARCHAR(45) NOT NULL,
  INDEX `fk_WeaponHasKeyword_Weapon1_idx` (`Weapon_id` ASC) VISIBLE,
  INDEX `fk_WeaponHasKeyword_WeaponKeyword1_idx` (`WeaponKeyword_id` ASC) VISIBLE,
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
-- Table `mydb`.`WeaponHasAbility`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`WeaponHasAbility` (
  `Weapon_id` VARCHAR(45) NOT NULL,
  `WeaponAbility_id` VARCHAR(45) NOT NULL,
  INDEX `fk_WeaponHasAbility_Weapon1_idx` (`Weapon_id` ASC) VISIBLE,
  INDEX `fk_WeaponHasAbility_WeaponAbility1_idx` (`WeaponAbility_id` ASC) VISIBLE,
  CONSTRAINT `fk_WeaponHasAbility_Weapon1`
    FOREIGN KEY (`Weapon_id`)
    REFERENCES `mydb`.`Weapon` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_WeaponHasAbility_WeaponAbility1`
    FOREIGN KEY (`WeaponAbility_id`)
    REFERENCES `mydb`.`WeaponAbility` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
