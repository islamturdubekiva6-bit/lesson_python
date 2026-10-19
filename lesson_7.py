class Animal:
    def __init__(self, name, species, age, weight, color):
        self.name = name        
        self.species = species  
        self.age = age          
        self.weight = weight    
        self.color = color      

    def make_sound(self):
        return f"{self.name} издаёт звук"

    def info(self):
        return (f"{self.name}: {self.species}, {self.age} лет, "
                f"{self.weight} кг, окрас - {self.color}")


class Reptile(Animal):
    """Пресмыкающиеся"""

    def __init__(self, name, species, age, weight, color,
                 is_venomous, body_length, molting_period):
        super().__init__(name, species, age, weight, color)
        self.is_venomous = is_venomous        
        self.body_length = body_length        
        self.molting_period = molting_period  

    def bask_in_sun(self):
        return f"{self.name} греется на солнце, чтобы поднять температуру тела"

    def molt(self):
        return (f"{self.name} линяет (раз в {self.molting_period} мес.) "
        f"и сбрасывает старую кожу")


class Amphibian(Animal):
    """Земноводные"""

    def __init__(self, name, species, age, weight, color, habitat, has_tail, larval_stage):
        super().__init__(name, species, age, weight, color)
        self.habitat = habitat            
        self.has_tail = has_tail          
        self.larval_stage = larval_stage  

    def swim(self):
        return f"{self.name} плывёт в воде ({self.habitat})"

    def breathe_through_skin(self):
        return f"{self.name} дышит через влажную кожу"

snake = Reptile("Как", "удав", 5, 12.0, "зелёный", False, 250, 3)
frog = Amphibian("Квакша", "лягушка", 2, 0.05, "зелёный", "пруд", False, "головастик")


print(snake.info())
print(snake.make_sound())
print(frog.info())
print(frog.make_sound())


print(snake.bask_in_sun())
print(snake.molt())
print(frog.swim())
print(frog.breathe_through_skin())