from asyncio import run

import asyncclick as click

from traveling_sso.database.deps import db_init_root_user


@click.group()
async def cli():
    pass


@cli.command()
@click.option(
    "--default-root-admin",
    is_flag=True,
    default=False,
    help="Use to create a root admin user with config from environment variables."
)
async def create_user(default_root_admin):
    if default_root_admin:
        await db_init_root_user()
        print("Default root admin user created.")
    else:
        print("Nothing's changed.")


if __name__ == "__main__":
    run(cli())
