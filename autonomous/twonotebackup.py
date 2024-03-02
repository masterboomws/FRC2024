from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state

class Autonomous(StatefulAutonomous):
    MODE_NAME = "TWONOTEBACKUP"

    def intialize(self):
        self.intial_called = None

    @timed_state(duration=2 , first=True, next_state="fire")
    def start(self):
        self.Shooter.shooterMotor.set(self.Shooter.shooterSpeed)

    @timed_state(duration=1, next_state="next")
    def fire(self):
        self.Intake.intakeMotorOne.set(-self.Intake.intakeOutSpeed)
        self.Intake.intakeMotorTwo.set(-self.Intake.intakeOutSpeed)

    @timed_state(duration=1, next_state="drive")
    def next(self):
        self.Shooter.shooterMotor.set(0)
        self.Intake.intakeMotorOne.set(0)
        self.Intake.intakeMotorTwo.set(0)
        self.Intake.pivotOnePosition = -7.5
        self.Intake.pivotTwoPosition = -7.5

    @timed_state(duration=1, next_state="lift")
    def drive(self):
        self.Intake.intakeMotorOne.set(self.Intake.intakeInSpeed)
        self.Intake.intakeMotorTwo.set(self.Intake.intakeInSpeed)
        self.DriveTrain.robotDrive.driveCartesian(0.3, 0, 0)

    @timed_state(duration=0.7, next_state="drive2")
    def lift(self):
        self.DriveTrain.robotDrive.driveCartesian(0, 0, 0)
        self.Intake.pivotOnePosition = 0.1
        self.Intake.pivotTwoPosition = 0.1
    
    @timed_state(duration=1.2, next_state="start2")
    def drive2(self):
        self.DriveTrain.robotDrive.driveCartesian(-0.3, 0, 0)

    @timed_state(duration=2 , next_state="fire2")
    def start2(self):
        self.DriveTrain.robotDrive.driveCartesian(0, 0, 0)
        self.Shooter.shooterMotor.set(self.Shooter.shooterSpeed)

    @timed_state(duration=1, next_state="stop")
    def fire2(self):
        self.Intake.intakeMotorOne.set(-self.Intake.intakeOutSpeed)
        self.Intake.intakeMotorTwo.set(-self.Intake.intakeOutSpeed)

    @timed_state(duration=1)
    def stop(self):
        self.Intake.intakeMotorOne.set(0)
        self.Intake.intakeMotorTwo.set(0)
        self.Shooter.shooterMotor.set(0)
    

