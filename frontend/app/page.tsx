// import Image from "next/image";
import Link from 'next/link';

// function createTable() {
//   const tableName = document.getElementById('table_name').value;
//   const schema = document.getElementById('schema').value;

//   fetch('http://127.0.0.1:5000/create', {
//       method: 'POST',
//       headers: {
//           'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ tableName: tableName, schema: schema }),
//   })
//   .then(response => response.text())
//   .then(data => {
//       document.getElementById('output').textContent = data;
//   })
//   .catch((error) => {
//       console.error('Error:', error);
//   });
// }

// function insertData() {
//   const tableName = document.getElementById('table_name_insert').value;
//   const columns = document.getElementById('columns').value;
//   const data = document.getElementById('data').value;

//   fetch('http://127.0.0.1:5000/insert', {
//       method: 'POST',
//       headers: {
//           'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ tableName: tableName, columns: columns, data: data }),
//   })
//   .then(response => response.text())
//   .then(data => {
//       document.getElementById('output').textContent = data;
//   })
//   .catch((error) => {
//       console.error('Error:', error);
//   });
// }


// function getData() {
//   const tableName = document.getElementById('table_name_get').value;

//   fetch('http://127.0.0.1:5000/getall', {
//       method: 'POST',
//       headers: {
//           'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ tableName: tableName }),
//   })
//   .then(response => response.text())
//   .then(data => {
//       document.getElementById('output').textContent = data;
//   })
//   .catch((error) => {
//       console.error('Error:', error);
//   });
// }


export default function Home() {
  
  return (
    <div>
      <header>
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bulma@1.0.2/css/bulma.min.css"
        />
      </header>

      <section className="hero is-fullheight has-background-white">
        <div className="hero-body">
          <div className="container is-centered">
            <div className="columns is-centered">

              <div id="box3" className="column box has-background-white is-flex is-flex-direction-column">
                <div className="has-text-centered">
                  <h3 className="subtitle is-3 level-item has-text-centered has-text-black">
                    Networks
                  </h3>
                  <p className="has-text-black">Explore available networks</p>
                </div>

                <div className="mt-auto has-text-centered">
                  <Link href="/more">
                    <button id="button2" className="button is-primary is-fullwidth">
                      View Networks
                    </button>
                  </Link>
                </div>
              </div>

              <div className="column has-text-black">
                <form className="box has-background-white has-text-black">
                  <div className="field has-background-white has-text-black">
                    <h3 className="subtitle is-3 level-item has-text-centered has-text-black">
                      Name
                    </h3>
                    <input
                      className="input has-background-white is-rounded is-medium has-text-black"
                      type="text"
                      placeholder="Enter your Name"
                    />
                  </div>

                  <div className="field has-background-white has-text-black">
                    <h3 className="subtitle is-3 level-item has-text-centered has-text-black">
                      LinkedIn
                    </h3>
                    <input
                      className="input has-background-white is-rounded is-medium has-text-black"
                      type="text"
                      placeholder="Enter your LinkedIn"
                    />
                  </div>

                  <div className="field">
                    <Link href="/more">
                      <button id="button2" className="button is-primary is-fullwidth mb-3">
                        Join Network
                      </button>
                    </Link>
                  </div>

                  <h3 className="subtitle is-3 level-item has-text-centered has-text-black">
                    Or
                  </h3>

                  <div className="field">
                    <Link href="/create">
                      <button id="button2" className="button is-primary is-fullwidth">
                        Create Network
                      </button>
                    </Link>
                  </div>
                </form>
              </div>

            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
