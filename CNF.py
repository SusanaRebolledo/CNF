# Combine method for DEL step
def combine(string, terminals):

  if len(string) > 1: # Caso de que la cadena restante sea de mas de 1 caracter

        # Tenemos que devolver el las combinaciones que hay entre el primer simbolo de la cadena, y las combinaciones
        # resultantes a partir del siguiente metodo de la cadena

        combinaciones = list()                             # Inicializamos la lista que devolveremos
        combinacionesRestantes = recorreString(string[1:]) # Obtenemos las combinaciones resultates del resto de la cadena

        # Primer caso: Solo el primer simbolo de la cadena
        combinaciones.append(string[0])

        for i in combinacionesRestantes:
            combinaciones.append(string[0] + i) # Segundo caso: El primer simbolo y cada una de las combinaciones restantes
            combinaciones.append(' ' + i)       # Tercer caso: Solo el resto de combinaciones

        return combinaciones # Devolvemos lo obtenido anteriormente

  elif len(string) > 0: 
    # Caso de que solo quede un caracter

    return string[0]



# Initial grammar
terminals = {"a", "b"}
non_terminals = {"A", "B", "S"}
start = "S"
P = {"S→ASB", "A→aAS|a|ε", "B→SbS|A|bb"}

# Auxiliar variables
# For TERM
SUB = ("₀₁₂₃₄₅₆₇₈₉")
sub_set = ("₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉")
new_non_TERM = "N"
term  = 0
terms = set()
terms_rules = set()

# For BIN
bins = 0
bin_set = set()
BIN = set() 

# For DEL
nullables = set()
deleted = set()

# For UNIT
UNIT = set()

# CNF production rules set
CNF = set()

print(P)
print("New rules:")
copy = P.copy()
####### START and TERM steps
for i in copy:
    count = 0

    # Get LHS
    x = i[count]
    count = count + 1
    lhs = ""
    while x != "→":
      lhs += x
      x = i[count]
      count = count + 1

    #Get RHS
    rhs = ""
    while count < len(i):
      x = i[count]

      # START
      if x == start:
        new_start = start + SUB[0]
        terminals.add(new_start)
        new_rule = new_start + "→" + start
        start = new_start
        CNF.add(new_rule)
        print("START: " + new_rule )

      # TERM
      next = count + 1
      if count != len(i) - 1 and i[next] != "|" and x in terminals:
        if x not in terms:
          terms.add(x)
          new_non_terminal = new_non_TERM + SUB[term]
          non_terminals.add(new_non_terminal)
          new_rule = new_non_terminal + "→" + x
          terms_rules.add(new_rule)
          CNF.add(new_rule)
          print("TERM: " + new_rule)
          x = new_non_terminal
          term = term + 1
            
        else:
          for z in terms_rules:
            if z[3] == x:
              new_non_terminal = z[0] + z[1]
              x = new_non_terminal

      # next symbol
      rhs = rhs +  x
      count = count + 1

    # review RHS
    new_rhs = ""
    pos = 0
    for r in rhs:
      n = rhs[pos]
      if n in terms:
        for z in terms_rules:
          if z[3] == n:
              new_non_terminal = z[0] + z[1]
              new_ch = new_non_terminal
        new_rhs = new_rhs + new_ch
      else:
        new_rhs += rhs[pos]
      next = pos + 1
      pos = pos + 1
    rhs = new_rhs
    # Add production rule
    new_rule = lhs + "→" + rhs
    CNF.add(new_rule)


####### BIN steps
copy = CNF.copy()
for i in copy:
    count = 0
    num_non_terminals_rhs = 0

    # Get LHS
    x = i[count]
    count = count + 1
    lhs = ""
    while x != "→":
        lhs += x
        x = i[count]
        count = count + 1

    # Check number of non-terminals in RHS
    rhs = ""
    while count != len(i):
        x = i[count]
        next = count + 1
        # Count non_terminals
        if x not in terminals:
            # length 1 non-terminals
            if x in non_terminals:
                num_non_terminals_rhs = num_non_terminals_rhs + 1
            # lenght 2 non-terminals
            if x == new_non_TERM:
                x = x + i[next]
                count = next
                num_non_terminals_rhs = num_non_terminals_rhs + 1
        # next symbol
        rhs = rhs +  x
        count = count + 1

        ###################################################
        # BIN
        news = 0
        new_lhs = ""
        new_rhs = ""
        new_non_BIN = ""
        non_l2 = ""
        old_lhs = ""
        if count == len(i) and len(lhs) == 1 and num_non_terminals_rhs > 2:
            # Delete rule to add uploaded
            CNF.remove(i)
            old_lhs = lhs
            indice = 0
            while indice != len(rhs):
                j = rhs[indice]
                next = indice + 1

                # Combined rules
                if j == "|":
                    j = rhs[next]
                    lhs = old_lhs
                    num_non_terminals_rhs = 0

                # Non-terminals length1
                elif j in non_terminals and num_non_terminals_rhs > 2:
                    new_non_BIN = lhs + SUB[bins]
                    new_rhs = j + new_non_BIN
                    bins = bins + 1
                    bin_set.add(new_non_BIN)
                    non_terminals.add(new_non_BIN)
                    new_rule = lhs + "→" + new_rhs
                    CNF.add(new_rule)
                    BIN.add(new_rule)
                    lhs = new_non_BIN
                    news = news + 1

                # Rules not to modify 
                elif j in non_terminals and rhs[next] == "|" and num_non_terminals_rhs  == 0:
                    num_non_terminals_rhs = 0
                    new_rule = old_lhs + "→" + j
                    CNF.add(new_rule)
                    BIN.add(new_rule)

                elif num_non_terminals_rhs  == 0:
                    new_rhs = j
                    ind = indice
                    # Get full length
                    while next != len(rhs) and rhs[next] != "|":
                        new_rhs = new_rhs + rhs[next]
                        next = next + 1
                        ind = ind + 1
                    indice = ind
                    new_rule = old_lhs + "→" + new_rhs
                    CNF.add(new_rule)
                    BIN.add(new_rule)

                # Non-terminals lenght != 1
                elif j == new_non_TERM and j != "|" and next != len(j) and num_non_terminals_rhs > 2:
                    non_l2 = j
                    ind = indice
                    # Get full length
                    while non_l2 not in non_terminals and next != len(j) and rhs[next] in SUB and rhs[next] != "|":
                        non_l2 = non_l2 + rhs[next]
                        next = next + 1
                        ind = ind + 1

                    new_non_BIN = lhs + SUB[bins]
                    new_rhs = non_l2 + new_non_BIN
                    bins = bins + 1
                    bin_set.add(new_non_BIN)
                    non_terminals.add(new_non_BIN)
                    new_rule = lhs + "→" + new_rhs
                    CNF.add(new_rule)
                    BIN.add(new_rule)
                    lhs = new_non_BIN
                    news = news + 1
                    indice = indice + next - 1

                # Iterate
                indice = indice + 1

print("BIN: ", BIN)
print(CNF)
new_rhs = ""

####### DEL steps
copy = CNF.copy()
# Check nullables
for i in copy:
    count = 0

    # Get LHS
    x = i[count]
    count = count + 1
    lhs = ""
    while x != "→":
        lhs += x
        x = i[count]
        count = count + 1

    #Get RHS
    rhs = ""
    while count != len(i):
        x = i[count]
   
        # next symbol
        rhs = rhs +  x
        count = count + 1

    # Check nullables (only initial terminals, so LHS length 1)
    if len(lhs) == 1 and lhs != start and rhs == "ε":
        nullables.add(lhs)    
        # Delete nullable rule
        CNF.remove(i)
        deleted.add(i)

print("DEL: ", deleted, " (deleted rule)")  


## Replace rules with nullable terminals
copy = CNF.copy()

while True:

  nonReplacedLHSNullables = True

  for i in copy:

    count = 0
    terminals_rhs = set()

    # Get LHS
    x = i[count]
    count = count + 1
    lhs = ""
    while x != "→":
        lhs += x 
        x = i[count]
        count = count + 1
       
    #Get RHS
    num_terminals_rhs = 0
    num_nullables_rhs = 0
    rhs = ""
    while count != len(i):
        x = i[count]

        # next symbol
        rhs = rhs +  x
        count = count + 1

    # Count non-terminals nullables
    for j in range(len(rhs)):
      
      next = j + 1
      p = rhs[j]
      
      if p in non_terminals:
        while next < len(rhs) and rhs[next] in sub_set:
          p += rhs[next]
          j = j + 1
          next = j + 1
          
        if p in nullables:
          num_nullables_rhs += len(p)

      else:
        num_terminals_rhs += 1  

    # Check if all non-terminals are nullables
    if num_nullables_rhs == len(rhs):
      new_rhs = combine(rhs, terminals)
      nullables.add(lhs)

      # Generate new combined rules adn delete empty ones
      for k in new_rhs:
        if k != "":
          new_rule = lhs + "→" + k
          CNF.add(new_rule)
          deleted.add(new_rule)
    
    if lhs in nullables:
      nonReplacedLHSNullables = False

  if not nonReplacedLHSNullables:
    break

print("DEL: ", deleted)

####### UNIT step
nonReplacedRules = list()
removables = set()
while True:
  
  nonReplacedLHSNonTerminals = True

  for i in copy:

    count = 0
    terminals_rhs = set()

    # Get LHS
    x = i[count]
    count = count + 1
    lhs = ""
    while x != "→":
        lhs += x 
        x = i[count]
        count = count + 1
       
    #Get RHS
    num_terminals_rhs = 0
    num_nullables_rhs = 0
    rhs = ""
    while count != len(i):
        x = i[count]

        # next symbol
        rhs = rhs +  x
        count = count + 1
    
    # Count number of symbols in RHs
    rhsCharacters = list()
    symbol = ''

    for j in range(len(rhs)):
      symbol += rhs[j]
      if rhs[j] in terminals or rhs[j] in non_terminals or rhs[j] == new_non_TERM:
        j = j + 1
        while j < len(rhs) and rhs[j] in sub_set:
          symbol += rhs[j]
          j = j + 1
        rhsCharacters.append(symbol)
      symbol = ''
    
    # Check reemplazable rules (RHS is string of T and N)
    if lhs in non_terminals and (rhsCharacters[0] in terminals or len(rhsCharacters) > 1):
      nonReplacedRules.append([lhs, rhs])

    # Check unitary rules Non-terminal -> Non-terminal
    if len(lhs) == 1 and len(rhsCharacters) == 1 and rhsCharacters[0] in non_terminals:
      removables.add(i)
      for j in nonReplacedRules:
        if j[0] == rhs:
          new_rule = lhs + "→" + j[1]
          CNF.add(new_rule)
          UNIT.add(new_rule)
          nonReplacedLHSNonTerminals = False  
  if not nonReplacedLHSNonTerminals:
    break

# Remove unitary rules
for z in removables:
  CNF.remove(z)

print("UNIT: ", UNIT)


###### Recompose production rules
copy = CNF.copy()
final_rules = set()
lefts = set()
for i in copy:
    count = 0
    # Get LHS
    x = i[count]
    count = count + 1
    lhs = ""
    while x != "→":
      lhs += x
      x = i[count]
      count = count + 1

    #Get RHS
    rhs = ""
    while count != len(i):
      x = i[count]
      # next symbol
      rhs = rhs +  x
      count = count + 1

    # Reunite
    if lhs in lefts:
      fin_copy = final_rules.copy()
      for z in fin_copy:
        countl = 0

        # Get LHS
        j = z[countl]
        countl = countl + 1
        lhsl = ""
        while j != "→":
          lhsl += j
          j = z[countl]
          countl = countl + 1

        if lhs == lhsl:
          
          #Get RHS
          rhsl = ""
          while countl != len(z):
            j = z[countl]
            # next symbol
            rhsl = rhsl +  j
            countl = countl + 1

          # Add 
          rhsl = rhsl + "|" + rhs
          new_rule = lhs + "→" + rhsl
          final_rules.remove(z)
          final_rules.add(new_rule)
    else:
      new_rule = lhs + "→" + rhs
      final_rules.add(new_rule)
      lefts.add(lhs)
CNF = final_rules

print("Final rules in CNF: ", CNF)