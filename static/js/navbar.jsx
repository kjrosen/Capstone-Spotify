'use strict';


function Search(props) {
    const query = {
        type: document.getElementById("query").value
    }

    function goSearch() {
        fetch("/search", {
            method: 'POST',
            body: JSON.stringify(query),
            headers: {
                'Content-Type': 'application/json',
            },
        })
    }

    return (
        <label htmlFor="searchInput">
            <input type="text" id="query" /><br />
            <button type="button" onClick={goSearch}>Search</button>
        </label>
    );
}


function login() {

    return (
        <div>
            <label>Log in
                <form action="/log_in" method="POST">
                    <label>
                        Email: <input type="text" name="email" /></label><br />
                    <label>
                        Password: <input type="password" name="password" /><br />
                    </label>
                    <button type="submit">Log In</button>
                </form>
            </label>
            <br />

            <label>Join
                <form action="/join_up" method="POST">
                    <label>
                        Email: <input type="text" name="email" /></label><br />
                    <label>
                        Password: <input type="password" name="password" /></label><br />
                    <label>
                        Username: <input type="text" name="name" /></label><br />
                    <button type="submit">Sign Up</button>
                </form>
            </label>
        </div>
    );
}