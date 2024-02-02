<a name="readme-top"></a>

<!-- [![Stargazers][stars-shield]][stars-url] -->
<!-- [![MIT License][license-shield]][license-url] -->
[![LinkedIn][linkedin-shield]][linkedin-url]
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://tagideas.camiloavil.com">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
  <br/>
  <h1 align="center">TagIdeas</h1>

  <p align="center">
    a project focused on learning and practicing fullstack development skills.
    <br />
    <a href="https://tagideas.camiloavil.com/docs"><strong>Explore the OpenAPI docs »</strong></a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#requirements">Requirements</a></li>
        <li><a href="#run-with-python-virtual-enviroment">Run with python virtual enviroment</a></li>
        <li><a href="#run-with-docker-container">Run with Docker container</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

"TagIdeas" is an application designed for storing and sharing ideas. With the flexibility to tag others, you can store thoughts in a way that suits you, and recipients of tags will receive email notifications for seamless collaboration and communication. Dive into a user-friendly platform that encourages creativity and collaboration through the simple yet powerful act of sharing ideas.

"TagIdeas" is a project focused on learning and practicing backend and frontend development skills, incorporating tools like SQLAlchemy. It enables the storage and sharing of short ideas with tags. Future plans include frontend development using Vue or Svelte.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

"TagIdeas" is crafted using Python, with the backend structured on the robust FastAPI framework, ensuring efficient API development. The integration of SQLAlchemy as the ORM facilitates seamless database management. Additionally, the project employs the "fastapiusers" library for a streamlined user experience, enhancing authentication and user-related functionalities.
<br/>
- [![Python][Python]][Python-url]
- [![FastAPI][FastAPI]][FastAPI-url]
- [![SQLAlchemy][SQLAlchemy]][SQLAlchemy-url]
- [![fastapiusers][fastapiusers]][fastapiusers-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To run "TagIdeas" locally, There are two methods available: using a Python virtual environment and utilizing Docker to build and run the container using the provided Dockerfile.

## Requirements

- Python 3.6+
- Docker

## Run with python virtual enviroment

Clone the Repository:
```
git clone https://github.com/camiloavil/tagIdeas
cd TagIdeas
```
Create and Activate Virtual Environment:
```
python -m venv venv
source venv/bin/activate
```
Install Dependencies:
```
pip install -r requirements.txt
```
Set Environment Variables:
```
APP_NAME="TagIdeas" APP_GOOGLE_CLIENT_ID="client ID from Google"
```
Run the Application:
```
python main.py
```

## Run with Docker container

the easy way to run "tagIdeas" is in a docker container. you can create a `docker-compose.yml` like the next example. and run it.

### docker-compose.yml
```
services:
  tagideas:
    container_name: TagIdeas
    build:
      context: .
    ports:
      - "8000:8000"
    environment:
      - APP_NAME=tagIdeas
      - APP_GOOGLE_CLIENT_ID='client ID from Google'
      - APP_GOOGLE_CLIENT_SECRET='client secret from Google'
      - APP_LIFETIME=3600

```
### build and run container

```
docker compose up -d
```
<!-- USAGE EXAMPLES -->

## Usage

To run "TagIdeas" locally, it is essential to set specific environment variables, whether using the Docker container or executing with Python.

- `APP_NAME="TagIdeas"` &nbsp; _Name of the app_
- `PORT=8000` &nbsp; _Port on which the app runs_
- `APP_SECRET="PASS_SECRET"` &nbsp; _Secret key for app security_
- `APP_LIFETIME=3600` &nbsp; _Lifetime of the user session_
- `APP_GOOGLE_CLIENT_ID="ClientID app from Google"` &nbsp; _Google app's Client ID -  OAuth2_
- `APP_GOOGLE_CLIENT_SECRET="ClientSecret app from Google"` &nbsp; _Google app's Client Secret - OAuth2_


## Online Testing
You can also test "TagIdeas" online by visiting the url [https://tagideas.camiloavil.com](https://tagideas.camiloavil.com). Explore the application's features and experience seamless idea sharing and tagging in action!

_For more infomation about the API end points, please refer to the [Documentation](https://tagideas.camiloavil.com/docs)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [x] Set the API with FastAPI
- [x] Set user authentication using Bearer token and JWT with fastAPIusers
- [x] Add OAuth2 authentication
- [x] Set CRUD of Ideas models
- [x] Add relations of tagged users to Ideas models
- [ ] Integrate a frontend GUI using Vue or Svelte
  - [ ] Integrate login form whit OAuth2 Google "Google Sing In"
  - [ ] Implement the main app design displaying ideas and tags
- [ ] Implement a background task to send emails when a user is tagged in an idea

<!-- See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues). -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

**Contributions** are the essence of the open-source community, fostering learning, inspiration, and creation. Your contributions are highly valued.

If you have ideas to improve this project, fork the repository and submit a pull request. Alternatively, open an issue labeled "enhancement." Don't forget to star the project. Thank you once more!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/MyFeature`)
3. Commit your Changes (`git commit -m 'Add some MyFeature'`)
4. Push to the Branch (`git push origin feature/MyFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Camilo Avila - [@camilo_avil](https://twitter.com/camilo_avil) - camilo.avil@gmail.com

Project Link: [https://github.com/camiloavil/tagIdeas](https://github.com/camiloavil/tagIdeas)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

Big shoutouts to the awesome tools that made this project possible! A huge thanks to:

- [FastAPI][FastAPI-url]
- [FastAPIUsers][fastapiusers-url]
- [SQLAlchemy][SQLAlchemy-url]

you guys rock! Your incredible work laid the groundwork for so many projects, and I'm stoked to give credit where it's due. Much love! 🚀💙

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/camilo-avila-3a3567272/

[Python]: https://img.shields.io/badge/python-35495E?style=for-the-badge&logo=python&logoColor=4FC08D
[Python-url]: https://www.python.org/
[FastAPI]: https://img.shields.io/badge/fastapi-35495E?style=for-the-badge&logo=fastapi&logoColor=4FC08D
[FastAPI-url]: https://fastapi.tiangolo.com/
[SQLAlchemy]: https://img.shields.io/badge/sqlalchemy-35495E?style=for-the-badge&logo=sqlalchemy&logoColor=4FC08D
[SQLAlchemy-url]: https://www.sqlalchemy.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[fastapiusers]: https://img.shields.io/badge/FastAPIUsers-35495E?style=for-the-badge
[fastapiusers-url]: https://github.com/fastapi-users/fastapi-users

