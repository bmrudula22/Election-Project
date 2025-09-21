from consituency import get_constituencies   
from voter import generate_voters
from candidate import generate_candidates
from Polling_booth import generate_polling_booths
import numpy as np
import random


def main():
    random.seed(42)
    np.random.seed(42)
    
    print("🚀 Starting synthetic dataset generation...")

    df_const = get_constituencies()
    df_voters = generate_voters()
    df_candidates = generate_candidates()
    df_booths = generate_polling_booths()

    print("✅ All datasets generated successfully!")

if __name__ == "__main__":
    main()
