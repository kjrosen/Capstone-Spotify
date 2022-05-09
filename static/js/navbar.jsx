'use strict';


function InputBox(props) {
	return (
		<form>
				<input type='text' name={props.name}></input>
			<button onClick={props.event}>{props.name}</button>
		</form>
	);
}


function LogBox() {
	return (
		<form action='/join' method='POST' class='container' id='login'>
			<label class='row' for='email'>Email:<br/>
				<input type='text' id='email'></input>
			</label>
			<label class='row' for='pw'>Password:<br/>
				<input type='password' id='pw'></input>
			</label>
			<button type='submit'>Login</button>
		</form>
	);
}

function JoinBox() {
	return (
		<form action='/join' method='POST' class='container' id='join'>
			<label class='row' for='email'>Email:<br/>
				<input type='text' id='email'></input>
			</label>
			<label class='row' for='name'>Username:<br/>
				<input type='text' id='name'></input>
			</label>
			<label class='row' for='pw'>Password:<br/>
				<input type='password' id='pw'></input>
			</label>
			<button type='submit'>Join</button>
		</form>
	);
}

const SignBoxes = (
	<div>
		<LogBox />
		<JoinBox />
	</div>
);


function SendPlaylistPhrase() {

}


function SendDBQuery() {


}


function EmbedPlay(props) {
	return (
		<iframe src={props.playId} style='border-radius:12px' width='100%' height='380' frameBorder='0' allowFullScreen='' allow='autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture' />
	);
}


function PlaylistListItem(props) {
	return (
		<li id={props.playId}>{props.name} by {props.userName}</li>
	);
}

function ListedPlaylists(props) {

}







// join option only appears in navbar if user isn't already logged in
let joiner = document.querySelectorAll('#joiner');
if (joiner.length > 0) {
	joiner = ReactDom.createRoot(joiner[0])
}

const maker = ReactDom.createRoot(document.getElementById('maker'));
const makeBox = <InputBox name='New' event={SendPlaylistPhrase} />;

const searcher = ReactDom.createRoot(document.getElementById('searcher'));
const searchBox = <InputBox name='Search' event={SendDBQuery}/>;

const embeddedPlay = <EmbedPlay playId='' />
//embeddedPlay src  will always be dependent on
//1 - json data from makeBox fetch event OR
//2 - li id info from any of the listed playlist events