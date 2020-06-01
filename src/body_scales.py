class bodyScales:
    def __init__(self, age, height, sex, weight, scaleType='xiaomi'):
        self.age = age
        self.height = height
        self.sex = sex
        self.weight = weight

        if scaleType == 'xiaomi':
            self.scaleType = 'xiaomi'
        else:
            self.scaleType = 'holtek'

    # Get BMI scale
    def getBMIScale(self):
        if self.scaleType == 'xiaomi':
            # Amazfit/new mi fit
            #return [18.5, 24, 28]
            # Old mi fit // amazfit for body figure
            return [18.5, 25.0, 28.0, 32.0]
        elif self.scaleType == 'holtek':
            return [18.5, 25.0, 30.0]

    # Get fat percentage scale
    def getFatPercentageScale(self):
        # The included tables where quite strange, maybe bogus, replaced them with better ones...
        if self.scaleType == 'xiaomi':
            scales = [
                {'min': 0, 'max': 12, 'female': [12.0, 21.0, 30.0, 34.0], 'male': [7.0, 16.0, 25.0, 30.0]},
                {'min': 12, 'max': 14, 'female': [15.0, 24.0, 33.0, 37.0], 'male': [7.0, 16.0, 25.0, 30.0]},
                {'min': 14, 'max': 16, 'female': [18.0, 27.0, 36.0, 40.0], 'male': [7.0, 16.0, 25.0, 30.0]},
                {'min': 16, 'max': 18, 'female': [20.0, 28.0, 37.0, 41.0], 'male': [7.0, 16.0, 25.0, 30.0]},
                {'min': 18, 'max': 40, 'female': [21.0, 28.0, 35.0, 40.0], 'male': [11.0, 17.0, 22.0, 27.0]},
                {'min': 40, 'max': 60, 'female': [22.0, 29.0, 36.0, 41.0], 'male': [12.0, 18.0, 23.0, 28.0]},
                {'min': 60, 'max': 100, 'female': [23.0, 30.0, 37.0, 42.0], 'male': [14.0, 20.0, 25.0, 30.0]},
            ]

        elif self.scaleType == 'holtek':
            scales = [
                {'min': 0, 'max': 21, 'female': [18, 23, 30, 35], 'male': [8, 14, 21, 25]},
                {'min': 21, 'max': 26, 'female': [19, 24, 30, 35], 'male': [10, 15, 22, 26]},
                {'min': 26, 'max': 31, 'female': [20, 25, 31, 36], 'male': [11, 16, 21, 27]},
                {'min': 31, 'max': 36, 'female': [21, 26, 33, 36], 'male': [13, 17, 25, 28]},
                {'min': 36, 'max': 41, 'female': [22, 27, 34, 37], 'male': [15, 20, 26, 29]},
                {'min': 41, 'max': 46, 'female': [23, 28, 35, 38], 'male': [16, 22, 27, 30]},
                {'min': 46, 'max': 51, 'female': [24, 30, 36, 38], 'male': [17, 23, 29, 31]},
                {'min': 51, 'max': 56, 'female': [26, 31, 36, 39], 'male': [19, 25, 30, 33]},
                {'min': 56, 'max': 100, 'female': [27, 32, 37, 40], 'male': [21, 26, 31, 34]},
            ]

        for scale in scales:
            if self.age >= scale['min'] and self.age < scale['max']:
                return scale[self.sex]

    # Get muscle mass scale
    def getMuscleMassScale(self):
        if self.scaleType == 'xiaomi':
            scales = [
                {'min': {'male': 170, 'female': 160}, 'female': [36.5, 42.6], 'male': [49.4, 59.5]},
                {'min': {'male': 160, 'female': 150}, 'female': [32.9, 37.6], 'male': [44.0, 52.5]},
                {'min': {'male': 0, 'female': 0}, 'female': [29.1, 34.8], 'male': [38.5, 46.6]},
            ]
        elif self.scaleType == 'holtek':
            scales = [
                {'min': {'male': 170, 'female': 170}, 'female': [36.5, 42.5], 'male': [49.5, 59.4]},
                {'min': {'male': 160, 'female': 160}, 'female': [32.9, 37.5], 'male': [44.0, 52.4]},
                {'min': {'male': 0, 'female': 0}, 'female': [29.1, 34.7], 'male': [38.5, 46.5]}
            ]

        for scale in scales:
            if self.height >= scale['min'][self.sex]:
                return scale[self.sex]



    # Get water percentage scale
    def getWaterPercentageScale(self):
        if self.scaleType == 'xiaomi':
            if self.sex == 'male':
                return [55.0, 65.1]
            elif self.sex == 'female':
                return [45.0, 60.1]
        elif self.scaleType == 'holtek':
            return [53, 67]


    # Get visceral fat scale
    def getVisceralFatScale(self):
        # Actually the same in mi fit/amazfit and holtek's sdk
        return [10.0, 15.0]


    # Get bone mass scale
    def getBoneMassScale(self):
        if self.scaleType == 'xiaomi':
            scales = [
                {'male': {'min': 75.0, 'scale': [2.0, 4.2]}, 'female': {'min': 60.0, 'scale': [1.8, 3.9]}},
                {'male': {'min': 60.0, 'scale': [1.9, 4.1]}, 'female': {'min': 45.0, 'scale': [1.5, 3.8]}},
                {'male': {'min': 0.0, 'scale': [1.6, 3.9]}, 'female': {'min': 0.0, 'scale': [1.3, 3.6]}},
            ]

            for scale in scales:
                if self.weight >= scale[self.sex]['min']:
                    return scale[self.sex]['scale']

        elif self.scaleType == 'holtek':
            scales = [
                {'female': {'min': 60, 'optimal': 2.5}, 'male': {'min': 75, 'optimal': 3.2}},
                {'female': {'min': 45, 'optimal': 2.2}, 'male': {'min': 69, 'optimal': 2.9}},
                {'female': {'min': 0, 'optimal': 1.8}, 'male': {'min': 0, 'optimal': 2.5}}
            ]

            for scale in scales:
                if self.weight >= scale[self.sex]['min']:
                    return [scale[self.sex]['optimal']-1, scale[self.sex]['optimal']+1]


    # Get BMR scale
    def getBMRScale(self):
        if self.scaleType == 'xiaomi':
            coefficients = {
                'male': {30: 21.6, 50: 20.07, 100: 19.35},
                'female': {30: 21.24, 50: 19.53, 100: 18.63}
            }
        elif self.scaleType == 'holtek':
            coefficients = {
                'female': {12: 34, 15: 29, 17: 24, 29: 22, 50: 20, 120: 19},
                'male': {12: 36, 15: 30, 17: 26, 29: 23, 50: 21, 120: 20}
            }

        for age, coefficient in coefficients[self.sex].items():
            if self.age < age:
                return [self.weight * coefficient]


    # Get protein scale (hardcoded in mi fit)
    def getProteinPercentageScale(self):
        # Actually the same in mi fit and holtek's sdk
        return [16, 20]

    # Get ideal weight scale (BMI scale converted to weights)
    def getIdealWeightScale(self):
        scale = []
        for bmiScale in self.getBMIScale():
            scale.append((bmiScale*self.height)*self.height/10000)
        return scale

    # Get Body Score scale
    def getBodyScoreScale(self):
        # very bad, bad, normal, good, better
        return [50.0, 60.0, 80.0, 90.0]

    # Return body type scale
    def getBodyTypeScale(self):
        return ['obese', 'overweight', 'thick-set', 'lack-exerscise', 'balanced', 'balanced-muscular', 'skinny', 'balanced-skinny', 'skinny-muscular']

