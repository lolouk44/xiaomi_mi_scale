
# Reverse engineered from amazfit's app (also known as Mi Fit)
from body_scales import bodyScales
class bodyScore:

    def __init__(self, age, sex, height, weight, bmi, bodyfat, muscle, water, visceral_fat, bone, basal_metabolism, protein):
        self.age = age
        self.sex = sex
        self.height = height
        self.weight = weight
        self.bmi = bmi
        self.bodyfat = bodyfat
        self.muscle = muscle
        self.water = water
        self.visceral_fat = visceral_fat
        self.bone = bone
        self.basal_metabolism = basal_metabolism
        self.protein = protein
        self.scales = bodyScales(age, height, sex, weight)

    def getBodyScore(self):
        score = 100
        score -= self.getBmiDeductScore()
        score -= self.getBodyFatDeductScore()
        score -= self.getMuscleDeductScore()
        score -= self.getWaterDeductScore()
        score -= self.getVisceralFatDeductScore()
        score -= self.getBoneDeductScore()
        score -= self.getBasalMetabolismDeductScore()
        if self.protein:
            score -= self.getProteinDeductScore()
        return score

    def getMalus(self, data, min_data, max_data, max_malus, min_malus):
        result = ((data - max_data) / (min_data - max_data)) * float(max_malus - min_malus)
        if result >= 0.0:
            return result
        return 0.0

    def getBmiDeductScore(self):
        if not self.height >= 90:
            # "BMI is not reasonable
            return 0.0

        bmi_low = 15.0
        bmi_verylow = 14.0
        bmi_normal = 18.5
        bmi_overweight = 28.0
        bmi_obese = 32.0
        fat_scale = self.scales.getFatPercentageScale()

        # Perfect range (bmi >= 18.5 and bodyfat not high for adults, bmi >= 15.0 for kids
        if self.bmi >= 18.5 and self.age >= 18 and self.bodyfat < fat_scale[2]:
            return 0.0
        elif self.bmi >= bmi_verylow and self.age < 18 and self.bodyfat < fat_scale[2]:
            return 0.0

        # Extremely skinny (bmi < 14)
        elif self.bmi <= bmi_verylow:
            return 30.0
        # Too skinny (bmi between 14 and 15)
        elif self.bmi > bmi_verylow and self.bmi < bmi_low:
            return self.getMalus(self.bmi, bmi_verylow, bmi_low, 30, 15) + 15.0
        # Skinny (for adults, between 15 and 18.5)
        elif self.bmi >= bmi_low and self.bmi < bmi_normal and self.age >= 18:
            return self.getMalus(self.bmi, 15.0, 18.5, 15, 5) + 5.0

        # Normal or high bmi but too much bodyfat
        elif ((self.bmi >= bmi_low and self.age < 18) or (self.bmi >= bmi_normal and self.age >= 18)) and self.bodyfat >= fat_scale[2]:
            # Obese
            if self.bmi >= bmi_obese:
                return 10.0
            # Overweight
            if self.bmi > bmi_overweight:
                return self.getMalus(self.bmi, 28.0, 25.0, 5, 10) + 5.0
            else:
                return 0.0

    def getBodyFatDeductScore(self):
        scale = self.scales.getFatPercentageScale()

        if self.sex == 'male':
            best = scale[2] - 3.0
        elif self.sex == 'female':
            best = scale[2] - 2.0

        # Slighly low in fat or low part or normal fat
        if self.bodyfat >= scale[0] and self.bodyfat < best:
            return 0.0
        elif self.bodyfat >= scale[3]:
            return 20.0
        else:
            # Sightly high body fat
            if self.bodyfat < scale[3]:
                return self.getMalus(self.bodyfat, scale[3], scale[2], 20, 10) + 10.0

            # High part of normal fat
            elif self.bodyfat <= scale[2]:
                return self.getMalus(self.bodyfat, scale[2], best, 3, 9) + 3.0

            # Very low in fat
            elif self.bodyfat < scale[0]:
                return self.getMalus(self.bodyfat, 1.0, scale[0], 3, 10) + 3.0


    def getMuscleDeductScore(self):
        scale = self.scales.getMuscleMassScale()

        # For some reason, there's code to return self.calculate(muscle, normal[0], normal[0]+2.0, 3, 5) + 3.0
        # if your muscle is between normal[0] and normal[0] + 2.0, but it's overwritten with 0.0 before return
        if self.muscle >= scale[0]:
            return 0.0
        elif self.muscle < (scale[0] - 5.0):
            return 10.0
        else:
            return self.getMalus(self.muscle, scale[0] - 5.0, scale[0], 10, 5) + 5.0

    # No malus = normal or good; maximum malus (10.0) = less than normal-5.0;
    # malus = between 5 and 10, on your water being between normal-5.0 and normal
    def getWaterDeductScore(self):
        scale = self.scales.getWaterPercentageScale()

        if self.water >= scale[0]:
            return 0.0
        elif self.water <= (scale[0] - 5.0):
            return 10.0
        else:
            return self.getMalus(self.water, scale[0] - 5.0, scale[0], 10, 5) + 5.0

    # No malus = normal; maximum malus (15.0) = very high; malus = between 10 and 15
    # with your visceral fat in your high range
    def getVisceralFatDeductScore(self):
        scale = self.scales.getVisceralFatScale()

        if self.visceral_fat < scale[0]:
            # For some reason, the original app would try to
            # return 3.0 if vfat == 8 and 5.0 if vfat == 9
            # but i's overwritten with 0.0 anyway before return
            return 0.0
        elif self.visceral_fat >= scale[1]:
            return 15.0
        else:
            return self.getMalus(self.visceral_fat, scale[1], scale[0], 15, 10) + 10.0

    def getBoneDeductScore(self):
        scale = self.scales.getBoneMassScale()

        if self.bone >= scale[0]:
            return 0.0
        elif self.bone <= (scale[0] - 0.3):
            return 10.0
        else:
            return self.getMalus(self.bone, scale[0] - 0.3, scale[0], 10, 5) + 5.0

    def getBasalMetabolismDeductScore(self):
        # Get normal BMR
        normal = self.scales.getBMRScale()[0]

        if self.basal_metabolism >= normal:
            return 0.0
        elif self.basal_metabolism <= (normal - 300):
            return 6.0
        else:
            # It's really + 5.0 in the app, but it's probably a mistake, should be 3.0
            return self.getMalus(self.basal_metabolism, normal - 300, normal, 6, 3) + 5.0


    # Get protein percentage malus
    def getProteinDeductScore(self):
        # low: 10,16; normal: 16,17
        # Check limits
        if self.protein > 17.0:
            return 0.0
        elif self.protein < 10.0:
            return 10.0
        else:
            # Return values for low proteins or normal proteins
            if self.protein <= 16.0:
                return self.getMalus(self.protein, 10.0, 16.0, 10, 5) + 5.0
            elif self.protein <= 17.0:
                return self.getMalus(self.protein, 16.0, 17.0, 5, 3) + 3.0
