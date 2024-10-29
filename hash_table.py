import random
import pandas as pd
import hashlib
import matplotlib.pyplot as plt


județe = {
    "Alba": 1, "Arad": 2, "Argeș": 3, "Bacău": 4, "Bihor": 5, "Bistrița-Năsăud": 6, "Botoșani": 7,
    "Brașov": 8, "Brăila": 9, "Buzău": 10, "Caraș-Severin": 11, "Cluj": 12, "Constanța": 13,
    "Covasna": 14, "Dâmbovița": 15, "Dolj": 16, "Galați": 17, "Gorj": 18, "Harghita": 19,
    "Hunedoara": 20, "Ialomița": 21, "Iași": 22, "Ilfov": 23, "Maramureș": 24, "Mehedinți": 25,
    "Mureș": 26, "Neamț": 27, "Olt": 28, "Prahova": 29, "Satu Mare": 30, "Sălaj": 31,
    "Sibiu": 32, "Suceava": 33, "Teleorman": 34, "Timiș": 35, "Tulcea": 36, "Vaslui": 37,
    "Vâlcea": 38, "Vrancea": 39, "București": 40, "Călărași": 51, "Giurgiu": 52
}


prenume_masculine = [
    "Andrei", "Mihai", "Alexandru", "Vasile", "Ion", "Daniel", "Florin", "George",
    "Radu", "Claudiu", "Cristian", "Sergiu", "Lucian", "Paul", "Darius", "Robert",
    "Marius", "Stefan", "Nicolae", "Adrian", "Silvian", "Emilian", "Tudor", "Florentin",
    "Gabi", "Zsolt", "Mircea", "Victor", "Alin", "Iulian", "Ovidiu", "Cătălin",
    "Răzvan", "Cezar", "Dacian", "Ilie", "Virgil", "Mihăiță", "Traian", "Eugen",
    "Cornel", "Sorin", "Emil", "Răducu", "Grigore", "Ciprian", "Bogdan", "Petre",
    "Teodor", "Filip", "Doru", "Remus", "Nicu", "Valentin", "Vlad", "Ionuț"
]

prenume_feminine = [
    "Elena", "Ioana", "Maria", "Ana", "Irina", "Georgiana", "Andreea", "Daniela",
    "Roxana", "Mihaela", "Claudia", "Sonia", "Camelia", "Laura", "Adriana", "Anca",
    "Gabriela", "Diana", "Nicoleta", "Raluca", "Bianca", "Viorica", "Florentina",
    "Liliana", "Alina", "Simona", "Mirela", "Ramona", "Corina", "Olivia", "Irina",
    "Elisabeta", "Teodora", "Carmen", "Aurora", "Patricia", "Veronica", "Sofia",
    "Amalia", "Cecilia", "Marcela", "Felicia", "Madalina", "Eugenia", "Denisa",
    "Sabina", "Nadia", "Tatiana", "Adela", "Dorina", "Otilia", "Melania", "Zina"
]


nume_familie = [
    "Popescu", "Ionescu", "Dumitrescu", "Popa", "Stanciu", "Diaconu", "Tudor",
    "Marin", "Gheorghe", "Stoica", "Iliescu", "Stan", "Constantin", "Nistor",
    "Cristea", "Munteanu", "Radu", "Voicu", "Nicolescu", "Toma"
]

def genereaza_cnp(sex, an, luna, zi, judet):
    S = 1 if sex == 'M' else 2 
    cod_judet = județe[judet]
    nnn = random.randint(1, 999)  

    cnp_fara_control = f"{S}{str(an)[-2:]:0>2}{luna:0>2}{zi:0>2}{cod_judet:0>2}{nnn:0>3}"
    control_weights = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]
    cifra_control = sum(int(cnp_fara_control[i]) * control_weights[i] for i in range(12)) % 11
    cifra_control = 1 if cifra_control == 10 else cifra_control

    return f"{cnp_fara_control}{cifra_control}"

persoane_tabel = []

for _ in range(1000):
    sex = random.choice(['M', 'F'])
    prenume = random.choice(prenume_masculine if sex == 'M' else prenume_feminine)
    nume_fam = random.choice(nume_familie)
    
    an = random.randint(1900, 2024)
    luna = random.randint(1, 12)
    zi = random.randint(1, 28)
    judet = random.choice(list(județe.keys()))
    
    cnp = genereaza_cnp(sex, an, luna, zi, judet)
    
    persoane_tabel.append({"prenume": prenume, "nume_familie": nume_fam, "sex": sex, "cnp": cnp})

df_persoane = pd.DataFrame(persoane_tabel)

print(df_persoane.head(1000))

persoane_mari = []

for _ in range(1_000_000):
    sex = random.choice(['M', 'F'])
    prenume = random.choice(prenume_masculine if sex == 'M' else prenume_feminine)
    nume_fam = random.choice(nume_familie)
    an = random.randint(1900, 2024)
    luna = random.randint(1, 12)
    zi = random.randint(1, 28)
    judet = random.choice(list(județe.keys()))
    cnp = genereaza_cnp(sex, an, luna, zi, judet)
    persoane_mari.append({"prenume": prenume, "nume_familie": nume_fam, "sex": sex, "cnp": cnp})

class HashTable:
    def __init__(self, size=1000003):
        self.size = size
        self.table = [[] for _ in range(self.size)]
    
    def hash_function(self, cnp):
        return int(hashlib.sha256(cnp.encode()).hexdigest(), 16) % self.size
    
    def insert(self, persoana):
        index = self.hash_function(persoana["cnp"])
        self.table[index].append(persoana)
    
    def search(self, cnp):
        index = self.hash_function(cnp)
        for persoana in self.table[index]:
            if persoana["cnp"] == cnp:
                return persoana
        return None


hash_table = HashTable()
for persoana in persoane_mari:
    hash_table.insert(persoana)


cnp_uri_random = random.sample([p["cnp"] for p in persoane_mari], 1000)


found_count = 0
iterations = []

for cnp in cnp_uri_random:
    found = False
    index = hash_table.hash_function(cnp)
    for i, persoana in enumerate(hash_table.table[index]):
        if persoana["cnp"] == cnp:
            found = True
            iterations.append(i + 1)
            found_count += 1
            break


print(f"CNP-uri găsite: {found_count}")
print(f"Media numărului de iterații: {sum(iterations) / len(iterations)}")


plt.hist(iterations, bins=20, edgecolor='black')
plt.title("Distribuția numărului de iterații pentru căutare")
plt.xlabel("Număr de iterații")
plt.ylabel("Frecvență")
plt.show()
