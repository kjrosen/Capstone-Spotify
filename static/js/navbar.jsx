'use strict';

function MakeNavbar(){
  //check whether the user is logged in or not
  //if so, return a link to their playlists
  //if not, return a form that has a log in submit option (username/password)
  //and a create account submit option(username/password/email/spotify connection)
  //both change the session login info but don't redirect
  //rerendering will change what appears in this location to the my playlists link

  return (
    <span>
      <span id="create"> 
          New Playlist
      </span>
      <span id="search">
          Search
      </span>
      <span id="account"></span>
    </span>
  )
}//make all of those spans events in their own right
//that render the below functions

ReactDOM.render(<MakeNavbar />, document.querySelector('.navbar'));


function Create(){
  //render a form
  //take the input text and send it to python to split and search through spotify
  //render the completed playlist in .new_playlist

  return(
    <form className="popbar">
      <input type="text" />
      <button type="submit">Create</button>
    </form>
  );
}

function Search(){
  //render a search bar
  //perform a SQLquery for keywords searched
  //either title or artist hit within playlists
  //render list of playlists in .search_results

  return (
    <form className="popbar">
      <input type="text" />
      <button type="submit">Search</button>
    </form>
  );
}
