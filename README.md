# Pixo App Server 

Pixo App Server is the backend service for the Pixo application, a platform for managing and sharing items. This server handles user authentication, manages collectible items, and provides APIs for the front-end application.

## Description 

The Pixo App Server is built to support the Pixo web and mobile applications. It provides a RESTful API for user operations, collectible item management, and other functionalities necessary for a seamless user experience in the Pixo App.

### Dependencies 

- Front End - Javascript/React
- CSS - Tailwind & Radix
- Back End - Python/Django

## Installing

- git clone ```git@github.com:hi-michelleprimiani/pixo-api.git```
- cd to ```pixo-api```
- pip install
- pipenv shell
- open VSCODE project, start debugger

### User Login Info 
- username: BirdsOfAFeather
- password: password

## API Reference

- Details about the API endpoints and request/response formats

### Example EndPoint
- **Get Collectible Item** - GET ```http://localhost:8000/collectibles/:itemId```
- **Response** - JSON object containing collectible details

- **Get PixoUser** - GET ```http://localhost:8000/pixouser/:userId```
- **Response** - JSON object containing pixouser details and items listed

## Acknowledgements
- Special thanks to Etsy for providing a vibrant marketplace and community that inspired the user-centric design and functionality of the Pixo App.


