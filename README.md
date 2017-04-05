Functional specification:

- Users should be able to create an account and log in
- Users should be able to edit their profile page
- Users should be able to create projects, invite other user, or join other groups
- Users should be able to chat with other users in the same group
- Users should be able to upload and upload files, as well as delete them
- Users should be able to add comments on selected parts of an image
- Users should be able to create an invite link, linking directly to specified projects


Technological specification:

- Client framework: Vue.js
	- Client-side-routing: vue-router
	- HTTP client: Axios
	- State management: vuex
	- Build tool: Webpack + vue-loader
- Server framework: Flask
	- Database: MySQL
	- Real-time engine: SocketIO (Flask-SocketIO)