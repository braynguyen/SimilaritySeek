import Link from 'next/link';

// These styles apply to every route in the application
import './globals.css'
import {
  ClerkProvider,
  SignInButton,
  SignedIn,
  SignedOut,
  UserButton
} from '@clerk/nextjs'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en">
      <SignedIn>
        <body>
        <section className="hero is-small">
        <div className="navbar-menu">
          <div className="navbar-start">
            <div className="hero-body">
            <Link href="/">
              <p className="title">Network Search</p>
              <p className="subtitle">A New Way to Find People</p>
            </Link>
            </div>
          </div>

          <div className="navbar-end pr-5">
          <UserButton />
          </div>
        </div>
        </section>

        {children}
        </body>
      </SignedIn>

      <SignedOut>
        <body>
          <link
            rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/bulma@1.0.2/css/bulma.min.css"
          />
          <section className="hero has-background-white is-fullheight">
            <div className="hero-body is-flex is-justify-content-center is-align-items-center is-flex-direction-column">
              <div className="has-text-centered">
                <Link href="/">
                <h3 className="subtitle is-2 has-text-black">
                    Welcome, Please Sign in
                  </h3>
                  <h3 className="subtitle is-4 has-text-black">
                    Network Search
                  </h3>
                </Link>
              </div>
              <div className="mt-5">
                <button id="button2" className="button is-primary">
                  <SignInButton />
                </button>
              </div>
            </div>
          </section>
        </body>
      </SignedOut>

    </html>
    </ClerkProvider>
  )
}

//     <ClerkProvider>
//       <html lang="en">
//         <body>
          // <SignedOut>
          //   <SignInButton />
          // </SignedOut>

//           <SignedIn>
//             <UserButton />
//           </SignedIn>

//           {children}
//         </body>
//       </html>
//     </ClerkProvider>
//   )
// }