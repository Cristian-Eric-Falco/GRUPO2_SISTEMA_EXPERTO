class Body(Fact):
    """Hecho inicial con medidas corporales"""
    pass

class BodyTypeEngine(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.trace_msgs = []
        self.trace_keys = []
        self.tipo_final = None

    # --- Reglas Intermedias ---

    @Rule(Body(grasa=MATCH.g), TEST(lambda g: g < 15), salience=10)
    def grasa_baja(self, g):
        self.trace_msgs.append(f"Detectado: grasa baja ({g} < 15)")
        self.trace_keys.append("grasa_baja")
        self.declare(Fact(grasa_baja=True))

    @Rule(Body(grasa=MATCH.g), TEST(lambda g: 15 <= g < 18), salience=10)
    def grasa_media(self, g):
        self.trace_msgs.append(f"Detectado: grasa media ({g} entre 15 y 18)")
        self.trace_keys.append("grasa_media")
        self.declare(Fact(grasa_media=True))

    @Rule(Body(grasa=MATCH.g), TEST(lambda g: g >= 18), salience=10)
    def grasa_alta(self, g):
        self.trace_msgs.append(f"Detectado: grasa alta ({g} $\geq$ 18)")
        self.trace_keys.append("grasa_alta")
        self.declare(Fact(grasa_alta=True))

    @Rule(Body(masa_muscular=MATCH.mm), TEST(lambda mm: mm < 30), salience=10)
    def masa_baja(self, mm):
        self.trace_msgs.append(f"Detectado: masa muscular baja ({mm} < 30)")
        self.trace_keys.append("masa_baja")
        self.declare(Fact(masa_baja=True))

    @Rule(Body(masa_muscular=MATCH.mm), TEST(lambda mm: mm >= 30), salience=10)
    def masa_alta(self, mm):
        self.trace_msgs.append(f"Detectado: masa muscular alta ({mm} $\geq$ 30)")
        self.trace_keys.append("masa_alta")
        self.declare(Fact(masa_alta=True))

    @Rule(Body(peso=MATCH.p), TEST(lambda p: p < 60), salience=10)
    def peso_bajo(self, p):
        self.trace_msgs.append(f"Detectado: peso bajo ({p} < 60)")
        self.trace_keys.append("peso_bajo")
        self.declare(Fact(peso_bajo=True))

    @Rule(Body(peso=MATCH.p), TEST(lambda p: 60 <= p <= 90), salience=10)
    def peso_medio(self, p):
        self.trace_msgs.append(f"Detectado: peso medio ({p} entre 60 y 90)")
        self.trace_keys.append("peso_medio")
        self.declare(Fact(peso_medio=True))

    @Rule(Body(peso=MATCH.p), TEST(lambda p: p > 90), salience=10)
    def peso_alto(self, p):
        self.trace_msgs.append(f"Detectado: peso alto ({p} > 90)")
        self.trace_keys.append("peso_alto")
        self.declare(Fact(peso_alto=True))


    # --- Reglas Finales ---

    @Rule(
        Fact(masa_baja=True),
        OR(
            Fact(grasa_baja=True),
            AND(
                Fact(grasa_media=True),
                OR(Fact(peso_bajo=True), Fact(peso_medio=True))
            )
        ),
        salience=1
    )
    def clasificar_ecto(self):
        self.trace_msgs.append("Clasificación: ECTOMORFO")
        self.trace_keys.append("ecto")
        self.tipo_final = 'ectomorfo'


    @Rule(
        Fact(masa_alta=True),
        OR(
            Fact(grasa_baja=True),
            AND(
                Fact(grasa_media=True),
                OR(Fact(peso_bajo=True), Fact(peso_medio=True))
            )
        ),
        salience=1
    )
    def clasificar_meso(self):
       self.trace_msgs.append("Clasificación: MESOMORFO")
       self.trace_keys.append("meso")
       self.tipo_final = 'mesomorfo'


    @Rule(
        OR(
            Fact(grasa_alta=True),
            AND(
                Fact(grasa_media=True),
                Fact(peso_alto=True)
            )
        ),
        salience=1
    )
    def clasificar_endo(self):
        self.trace_msgs.append("Clasificación: ENDOMORFO")
        self.trace_keys.append("endo")
        self.tipo_final = 'endomorfo'


    # --- Función Classify  ---

    def classify(self, peso: float, masa_muscular: float, grasa: float):
        self.reset()
        self.trace_msgs = []
        self.trace_keys = []
        self.tipo_final = None
        self.declare(Body(peso=peso, masa_muscular=masa_muscular, grasa=grasa))
        self.run()
        # Devuelve el tipo, los mensajes y las claves
        return self.tipo_final or 'indeterminado', self.trace_msgs, self.trace_keys