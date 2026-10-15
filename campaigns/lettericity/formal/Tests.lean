import Challenge
open Lettericity
example : targetWitness (⟨3, [(0,1),(1,2),(0,2)]⟩,1) ([0,1,2], [0,0,0], [(0,0)]) = true := by native_decide
example : targetWitness (⟨3, [(0,1)]⟩,1) ([0,1,2], [0,0,0], [(0,0)]) = false := by native_decide
