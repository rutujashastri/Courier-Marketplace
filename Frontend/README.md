### Project Setup

1. #### Installing Node
    An asynchronous event-driven JavaScript runtime having features like JSX support, JavaScript compiler and bundler. Node (>v14.0.0) comes with `npm` and `npx` and we will be using `npx create-react-app` command to generate basic structure of a react application. NPM is Node Package Manager which is helpful for managing different packages and their versions across different node projects.

    Confirm that Node is installed using command prompt, open command prompt and type -
    ```bash
    node -v
    ```
    and
    ```bash
    npm -v
    ```
    If you get some version printed on the console like `vxx.x.x` and `x.x.x`, then you have node installed on your machine. Then upgrade to latest version using
    command -
    ```bash
    nvm install latest
    ```
    Otherwise, you will need to install Node on your machine by going to [official Node.js download page](https://nodejs.org/en/download/) and then click on 'Current' tab and then download 'Windows Installer' (.msi file) or 'macOS Installer' (.pkg file) accordingly. Follow the instructions on the installation wizard without making any custom changes.

---

2. #### Cloning Git Repository (i.e. react app)
    Ensure that you have Git installed on your machine and configured with for your Git account.
    > Installing and setting up Git will be explain in other session.

    To clone (download) this repository, open the command prompt in the folder where you want to keep this project. Then enter the following command which will automatically download the repository -
    ```bash
    git clone https://github.com/fetchai/courier-marketplace
    ```
---

3. #### Installing Dependency Packages
    Open command prompt in the project folder -
    To download `node_modules` (where all the packages will be downloaded to run and build the react app) run following command -
    ```bash
    npm ci
    ```
    > Notice that, many tutorials suggest using `npm install` to install dependencies, but here `npm ci` specifies that the dependencies are **C**lean **I**nstalled with the versions prescribed in the package-lock.json file. It never writes to `package.json` or `package-lock.json`.
    New folder named `node_modules` (big sized!!!) will be created in the project folder, don't worry it won't be pushed to remote GitHub repository.

---

4. #### Running the React App
	Now all the configuration and dependencies are set up, it's time to run the react app.
    To run the react app, open the folder in VS Code and open New Terminal, then run the following command -
    ```bash
    npm run dev
    ```


# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
