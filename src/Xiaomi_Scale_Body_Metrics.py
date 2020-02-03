from math import floor
import sys
from body_scales import bodyScales

class bodyMetrics:
    def __init__(self, weight, height, age, sex, impedance):
        self.weight = weight
        self.height = height
        self.age = age
        self.sex = sex
        self.impedance = impedance
        self.scales = bodyScales(age, height, sex, weight)

        # Check for potential out of boundaries
        if self.height > 220:
            print("Height is too high (limit: >220cm) or scale is sleeping")
            sys.stderr.write('Height is over 220cm or scale is sleeping\n')
            exit()
        elif weight < 10 or weight > 200:
            print("Weight is either too low or too high (limits: <10kg and >200kg) or scale is sleeping")
            sys.stderr.write('Weight is above 10kg or below 200kg or scale is sleeping\n')
            exit()
        elif age > 99:
            print("Age is too high (limit >99 years) or scale is sleeping")
            sys.stderr.write('Age is above 99 years or scale is sleeping\n')
            exit()
        elif impedance > 3000:
            print("Impedance is above 3000ohm or scale is sleeping")
            sys.stderr.write('Impedance is above 3000ohm or scale is sleeping\n')
            exit()

    # Set the value to a boundary if it overflows
    def checkValueOverflow(self, value, minimum, maximum):
        if value < minimum:
            return minimum
        elif value > maximum:
            return maximum
        else:
            return value

    # Get LBM coefficient (with impedance)
    def getLBMCoefficient(self):
        lbm =  (self.height * 9.058 / 100) * (self.height / 100)
        lbm += self.weight * 0.32 + 12.226
        lbm -= self.impedance * 0.0068
        lbm -= self.age * 0.0542
        return lbm

    # Get BMR
    def getBMR(self):
        if self.sex == 'female':
            bmr = 864.6 + self.weight * 10.2036
            bmr -= self.height * 0.39336
            bmr -= self.age * 6.204
        else:
            bmr = 877.8 + self.weight * 14.916
            bmr -= self.height * 0.726
            bmr -= self.age * 8.976

        # Capping
        if self.sex == 'female' and bmr > 2996:
            bmr = 5000
        elif self.sex == 'male' and bmr > 2322:
            bmr = 5000
        return self.checkValueOverflow(bmr, 500, 10000)

    # Get fat percentage
    def getFatPercentage(self):
        # Set a constant to remove from LBM
        if self.sex == 'female' and self.age <= 49:
            const = 9.25
        elif self.sex == 'female' and self.age > 49:
            const = 7.25
        else:
            const = 0.8

        # Calculate body fat percentage
        LBM = self.getLBMCoefficient()

        if self.sex == 'male' and self.weight < 61:
            coefficient = 0.98
        elif self.sex == 'female' and self.weight > 60:
            coefficient = 0.96
            if self.height > 160:
                coefficient *= 1.03
        elif self.sex == 'female' and self.weight < 50:
            coefficient = 1.02
            if self.height > 160:
                coefficient *= 1.03
        else:
            coefficient = 1.0
        fatPercentage = (1.0 - (((LBM - const) * coefficient) / self.weight)) * 100

        # Capping body fat percentage
        if fatPercentage > 63:
            fatPercentage = 75
        return self.checkValueOverflow(fatPercentage, 5, 75)

    # Get water percentage
    def getWaterPercentage(self):
        waterPercentage = (100 - self.getFatPercentage()) * 0.7

        if (waterPercentage <= 50):
            coefficient = 1.02
        else:
            coefficient = 0.98

        # Capping water percentage
        if waterPercentage * coefficient >= 65:
            waterPercentage = 75
        return self.checkValueOverflow(waterPercentage * coefficient, 35, 75)

    # Get bone mass
    def getBoneMass(self):
        if self.sex == 'female':
            base = 0.245691014
        else:
            base = 0.18016894

        boneMass = (base - (self.getLBMCoefficient() * 0.05158)) * -1

        if boneMass > 2.2:
            boneMass += 0.1
        else:
            boneMass -= 0.1

        # Capping boneMass
        if self.sex == 'female' and boneMass > 5.1:
            boneMass = 8
        elif self.sex == 'male' and boneMass > 5.2:
            boneMass = 8
        return self.checkValueOverflow(boneMass, 0.5 , 8)

    # Get muscle mass
    def getMuscleMass(self):
        muscleMass = self.weight - ((self.getFatPercentage() * 0.01) * self.weight) - self.getBoneMass()

        # Capping muscle mass
        if self.sex == 'female' and muscleMass >= 84:
            muscleMass = 120
        elif self.sex == 'male' and muscleMass >= 93.5:
            muscleMass = 120

        return self.checkValueOverflow(muscleMass, 10 ,120)

    # Get Visceral Fat
    def getVisceralFat(self):
        if self.sex == 'female':
            if self.weight > (13 - (self.height * 0.5)) * -1:
                subsubcalc = ((self.height * 1.45) + (self.height * 0.1158) * self.height) - 120
                subcalc = self.weight * 500 / subsubcalc
                vfal = (subcalc - 6) + (self.age * 0.07)
            else:
                subcalc = 0.691 + (self.height * -0.0024) + (self.height * -0.0024)
                vfal = (((self.height * 0.027) - (subcalc * self.weight)) * -1) + (self.age * 0.07) - self.age
        else:
            if self.height < self.weight * 1.6:
                subcalc = ((self.height * 0.4) - (self.height * (self.height * 0.0826))) * -1
                vfal = ((self.weight * 305) / (subcalc + 48)) - 2.9 + (self.age * 0.15)
            else:
                subcalc = 0.765 + self.height * -0.0015
                vfal = (((self.height * 0.143) - (self.weight * subcalc)) * -1) + (self.age * 0.15) - 5.0

        return self.checkValueOverflow(vfal, 1 ,50)

    # Get BMI
    def getBMI(self):
        return self.checkValueOverflow(self.weight/((self.height/100)*(self.height/100)), 10, 90)

    # Get ideal weight (just doing a reverse BMI, should be something better)
    def getIdealWeight(self, orig=True):
        # Uses mi fit algorithm (or holtek's one)
        if orig and self.sex == 'female':
            return (self.height - 70) * 0.6
        elif orig and self.sex == 'male':
            return (self.height - 80) * 0.7
        else:
            return self.checkValueOverflow((22*self.height)*self.height/10000, 5.5, 198)

    # Get fat mass to ideal (guessing mi fit formula)
    def getFatMassToIdeal(self):
        mass = (self.weight * (self.getFatPercentage() / 100)) - (self.weight * (self.scales.getFatPercentageScale()[2] / 100))
        if mass < 0:
            return {'type': 'to_gain', 'mass': mass*-1}
        else:
            return {'type': 'to_lose', 'mass': mass}

    # Get protetin percentage (warn: guessed formula)
    def getProteinPercentage(self, orig=True):
        # Use original algorithm from mi fit (or legacy guess one)
        if orig:
            proteinPercentage = (self.getMuscleMass() / self.weight) * 100
            proteinPercentage -= self.getWaterPercentage()
        else:
            proteinPercentage = 100 - (floor(self.getFatPercentage() * 100) / 100)
            proteinPercentage -= floor(self.getWaterPercentage() * 100) / 100
            proteinPercentage -= floor((self.getBoneMass()/self.weight*100) * 100) / 100

        return self.checkValueOverflow(proteinPercentage, 5, 32)

    # Get body type (out of nine possible)
    def getBodyType(self):
        if self.getFatPercentage() > self.scales.getFatPercentageScale()[2]:
            factor = 0
        elif self.getFatPercentage() < self.scales.getFatPercentageScale()[1]:
            factor = 2
        else:
            factor = 1

        if self.getMuscleMass() > self.scales.getMuscleMassScale()[1]:
            return 2 + (factor * 3)
        elif self.getMuscleMass() < self.scales.getMuscleMassScale()[0]:
            return (factor * 3)
        else:
            return 1 + (factor * 3)

    # Get Metabolic Age
    def getMetabolicAge(self):
        if self.sex == 'female':
            metabolicAge = (self.height * -1.1165) + (self.weight * 1.5784) + (self.age * 0.4615) + (self.impedance * 0.0415) + 83.2548
        else:
            metabolicAge = (self.height * -0.7471) + (self.weight * 0.9161) + (self.age * 0.4184) + (self.impedance * 0.0517) + 54.2267
        return self.checkValueOverflow(metabolicAge, 15, 80)
