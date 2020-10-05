djangocms-template project is usable by itself. You can follow the local setup instructions to try it out. A live instance is configured within what. divio organization - https://control.divio.com/control/1820/edit/83288/


Divio Integration Setup
-------------------------------------------------------------------------------
- create a new project on divio without deploying it, set the type python3, django with default boilerplate
- create a new empty repository on git and add the following remotes:
    - `git remote add template git@gitlab.com:what-digital/djangocms-template.git`
    - `git remote add divio git@git.divio.com:{project-slug}.git`, replace `{project-slug}`, the project slug can be found in the project title and url:
        <details>
    
        ![](/docs/guidelines/img/project-slug.png)
    
        </details>
- run `git pull template master`
- run `git push --force divio master`
- make sure that your project and divio repositories are in sync, now switch divio to gitlab external repository according to [divio docs](https://docs.divio.com/en/latest/how-to/resources-configure-git/)
- set up a gitlab webhook
- compile the requirements (see the [setup instructions](/docs/setup-instruction.md))
- update .aldryn-example file with the values from the control page eg `https://control.divio.com/control/6215/edit/81016/` the id is `81016`
- enable mailtrap and sentry, see the instructions below
- remove the following files and content:
    - remove this section from `README.md`, along with the first sentence about djangocms-template independent setup
    - remove the `docs` directory - it should be stored only within this source repository
    - remove `base.Dockerfile`, `.gitlab-ci.yml`, `LICENSE`
    - if you're planning to use more than one CMS language go to [frontend/global/ts/ckeditor-config.js](/frontend/global/ts/ckeditor-config.js) and remove the `scayt_autoStartup = true` line
    - add the real stage domain to the last line about guest access in this readme.md file
- deploy the stage server
 
⚠ ️BEWARE: If you get a migration error on Divio deployment, follow the instructions for database reset placed in [setup instructions](https://gitlab.com/what-digital/djangocms-template/-/blob/master/docs/setup-instruction.md#how-to-drop-the-database)

### Mailtrap setup

- signup with a tech eamil, eg `tech+{project_name}@what.digital` https://mailtrap.io/register/signup
- save the login/password to the project's 1password vault, or send it to Victor / Mario, and add it to this REAMDE file
- add `EMAIL_URL` to the divio envs `smtps://{username}:{password}@smtp.mailtrap.io:2525`

### Sentry setup

- create a new account using tech email `tech+{project_name}@what.digital`
- save the login/password to the project's 1password vault, or send it to Victor / Mario
- add `SENTRY_DSN` to the divio envs


You can access the stage server without logging in through the url https://{domain}.aldryn.io/?guest-access=true

Development Setup
-------------------------------------------------------------------------------
Built on Python 3.7, Django 3.0, DjangoCMS 3.8, Webpack 4, TypeScript 3.

See the general [setup instructions](https://gitlab.com/what-digital/djangocms-template/-/blob/master/docs/setup-instruction.md)

[Project intro & guidelines](https://gitlab.com/what-digital/djangocms-template/-/blob/master/docs/README.md)
