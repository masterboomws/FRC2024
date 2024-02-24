import rev
from wpilib import SmartDashboard
from sim.spark_sim import CANSparkMax
from wpilib import SPI
from wpilib.drive import MecanumDrive
from navx import AHRS

from robot_map import CAN

class DriveTrain:
    def __init__(self, controller, LimeLight, JoystickCtrl):
        # Intializes motors for the drive basse.
        self.frontRightMotor = CANSparkMax(CAN.frontRightChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.rearRightMotor = CANSparkMax(CAN.rearRightChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.frontLeftMotor = CANSparkMax(CAN.frontLeftChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.rearLeftMotor = CANSparkMax(CAN.rearLeftChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.frontRightMotor.restoreFactoryDefaults()
        self.rearRightMotor.restoreFactoryDefaults()
        self.frontLeftMotor.restoreFactoryDefaults()
        self.rearLeftMotor.restoreFactoryDefaults()
        self.frontRightMotor.setInverted(True)
        self.rearRightMotor.setInverted(True)

        # Sets up the controller and drive train.
        self.controller = controller
        self.JoystickCtrl = JoystickCtrl
        self.robotDrive = MecanumDrive(self.frontLeftMotor, self.rearLeftMotor, self.frontRightMotor,
                                       self.rearRightMotor)
        self.gyroscope = AHRS(SPI.Port.kMXP)
        self.gyroscope.reset()
        self.LimeLight = LimeLight
        
    def autonomousInit(self):
        pass
    
    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        # Handles the movement of the drive base.
        if self.JoystickCtrl:
            self.robotDrive.driveCartesian(
                -self.controller.getY(),
                self.controller.getX(),
                self.controller.getZ(),
                -self.gyroscope.getRotation2d(),
            )
        else:
            self.robotDrive.driveCartesian(
                -self.controller.getLeftY(),
                self.controller.getLeftX(),
                self.controller.getRightX(),
                -self.gyroscope.getRotation2d(),
            )

            if self.controller.getBackButton():
                self.gyroscope.reset()
            if self.controller.getLeftBumper() and self.LimeLight.getNumber('tv'):
                self.pointAtTarget()
            if self.controller.getRightBumper() and self.LimeLight.getNumber('tv'):
                self.driveAtSpeaker()

        SmartDashboard.putNumber("yaw", self.gyroscope.getYaw())
    
    def pointAtTarget(self):
        '''points toward current limelight target. Returns cursor offset'''
        tx = self.LimeLight.getNumber('tx', 0)
        if tx > 0:
            self.robotDrive.driveCartesian(0, 0, 0, -tx / 30 + 0.05)
        elif tx < 0:
            self.robotDrive.driveCartesian(0, 0, 0, -tx / 30 - 0.05)
        return tx
    
    def driveAtSpeaker(self):
        '''drives toward speaker'''
        tx = self.LimeLight.getNumber('tx', 0)
        if tx > 0:
            turn_speed = -tx / 30 + 0.05
        elif tx < 0:
            turn_speed = -tx / 30 - 0.05
        
        ANGLE = 12
        diff = self.LimeLight.getNumber('ty') - ANGLE
        if diff > 0:
            drive_speed = -diff / 20 - 0.05
        elif diff < 0:
            drive_speed = -diff / 20 + 0.05
        if abs(tx) > 1 or abs(diff) > 1:
            self.robotDrive.driveCartesian(drive_speed, 0, 0, turn_speed)
        else:
            self.robotDrive.stopMotor()
