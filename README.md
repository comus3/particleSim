<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->






<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="IN-DEPTH-EXPLANATION">IN DEPTH EXPLANATION</a></li>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

My objectives for this project is to build a particle simulator that is deterministic fluid and fun to play with. To simulate newton's laws i used verlet equation.i implemeted it directly in the particle's methods.
collisions were hell to fix but they are currently working for the restraint and particle to particle collision is working but not fully optimised.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- IN DEPTH EXPLANATION -->
## IN DEPTH EXPLANATION

Le programme est conçu pour simuler la dynamique de particules en utilisant une mise en œuvre de l'équation de Verlet, une méthode numérique populaire pour résoudre les équations du mouvement. Cette méthode se distingue par sa stabilité et son aptitude à gérer les simulations de particules en interaction.

Lors de l'exécution du programme, les particules sont créées et initialement positionnées dans l'espace. Chaque particule possède des propriétés telles que sa position, sa vitesse, sa masse et sa charge électrique. Les particules peuvent être définies comme statiques ou mobiles, ce qui détermine si elles sont influencées par les forces externes.

La simulation est organisée en boucle, où chaque itération de la boucle représente un pas dans le temps. Voici comment le programme fonctionne :

1. **Initialisation :** Au démarrage, les paramètres de la simulation sont configurés. Cela inclut des variables telles que la durée entre les images (time_delta), le nombre de frames par seconde (frames), le rayon des particules, et d'autres valeurs nécessaires pour le calcul de la dynamique.

2. **Boucle de Simulation :** Le cœur du programme est la boucle de simulation. À chaque itération de la boucle, les étapes suivantes sont effectuées :

   a. **Gestion des Événements :** Le programme vérifie les événements en attente, tels que les interactions utilisateur avec des boutons ou des curseurs. Ces interactions peuvent ajouter de nouvelles particules ou ajuster les paramètres.

   b. **Calcul des Forces :** Différents effets et forces peuvent être appliqués aux particules. Ces forces peuvent inclure la gravité, des contraintes pour maintenir les particules dans certaines zones, et d'autres interactions.

   c. **Mise à Jour des Positions :** Chaque particule calcule sa nouvelle position en utilisant l'équation de Verlet, qui repose sur les positions actuelles et précédentes ainsi que les forces appliquées. Les particules mobiles sont déplacées en conséquence.

   d. **Détection de Collision :** La détection de collision est effectuée à l'aide d'une approche basée sur une grille. Les particules sont organisées dans une structure de grille pour accélérer la détection des collisions. Les particules qui se chevauchent sont corrigées en déplaçant leurs positions et en ajustant les vitesses en réponse à la collision.

   e. **Dessin :** Les positions mises à jour sont utilisées pour dessiner les particules sur l'écran, créant ainsi une représentation visuelle de la simulation.

   f. **Affichage :** L'écran est rafraîchi pour afficher les particules et les changements liés aux événements.

3. **Gestion des Paramètres :** Le programme offre des moyens d'interagir avec la simulation en ajustant les paramètres tels que la charge des particules, les effets appliqués, etc. Ces interactions peuvent être réalisées à l'aide de boutons et de curseurs, et elles peuvent influencer le comportement de la simulation.

En résumé, le programme simule la dynamique de particules en utilisant l'équation de Verlet pour mettre à jour les positions en fonction des forces appliquées. La détection de collision est gérée à travers une méthode basée sur une grille. Cette approche permet de visualiser les interactions entre les particules et de reproduire divers comportements de particules dans un environnement interactif.

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

not much for now

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] github
- [x] start project
- [x] implement dynamic
- [x] impleetn grav force or electric force
- [ ] add fun buttons and controls
- [ ] fluidify the whole thing
- [X] collisions
- [ ] make this library-able
- [ ] multi threading
- [ ] maybe find something else to display stuff


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

just find me!

<p align="right">(<a href="#readme-top">back to top</a>)</p>



