// import Image from "next/image";
import Link from 'next/link';

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
              <div className="column has-text-black ">
              <h1 className="subtitle is-1 has-text-black has-text-centered"> Create a network</h1>
                <form className="box has-background-white has-text-black">
                  <div className="field is-horizontal">
                    <div className="field-label is-normal">
                    <h3 className="subtitle is-4 has-text-black">
                    Network Name:
                  </h3>
                    </div>
                    <div className="field-body">
                      <div className="field">
                        <p className="control">
                          <input
                            className="input has-background-white is-rounded is-medium has-text-black"
                            type="text"
                            placeholder="Network Name"
                          />
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="field is-horizontal">
                    <div className="field-label is-normal">
                    <h3 className="subtitle is-4 has-text-black"> Name: </h3>
                    </div>
                    <div className="field-body">
                      <div className="field">
                        <p className="control">
                          <input
                            className="input has-background-white is-rounded is-medium has-text-black"
                            type="text"
                            placeholder="Name"
                          />
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Third Field */}
                  <div className="field is-horizontal">
                    <div className="field-label is-normal">
                    <h3 className="subtitle is-4 has-text-black"> Initial Members: </h3>
                    </div>
                    <div className="field-body">
                      <div className="field">
                        <p className="control">
                          <input
                            className="input has-background-white is-rounded is-medium has-text-black"
                            type="text"
                            placeholder="Initial Members"
                          />
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="columns is-full">
                    <div className="column">
                      <Link href="/more">
                        <button id="button1" className="button is-fullwidth">
                          Create Network
                        </button>
                      </Link>
                    </div>
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
