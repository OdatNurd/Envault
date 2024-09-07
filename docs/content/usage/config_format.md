---
title: Envault Configuration Format
description: Description of the Envault configuration format
---

The `Envault` configuration file is a [YAML](https://yaml.org/) formatted file
with a specific set of keys (outlined below) that is used to easily and
securely fetch down a set of environment variables and their values from a
remote server.

The official location to look for `Envault` configuration files is in a folder
named `envault`, which must be at the root of the project. Any `yml` files that
exist within this folder are assumed to be `Envault` configuration files and
can be used by the package.

When `Envault` loads a config file, it ensures that all of the keys outlined
below exist and have a (somewhat) sensible value; missing keys or keys that are
not set properly will generate an error.


## Configuration Keys

Each `Envault` configuration file must contain a set of predefined keys, which
are used to control how the package interacts with the `Envault` server (and
in fact specifies where to actually find that server).

### ^^apiKeyName^^

This specifies the **_name_** of an environment variable (which must already
exist and be set in your environment). When requests are made to the `Envault`
server, they use the value of that environment variable as the authentication
key on the request.

This allows for saving the configuration file into source control without
leaking the secret key that is used to make the `Envault` requests.


### ^^url^^

This specifies the base server URL that should be used to make the `Envault`
requests in order to fetch a set of environment variables.

Normally, this would be the default `Envault` server (which at the time of this
writing does not yet exist), although you can also self host your own server if
you would like to (for example, to have one in house).


### ^^vars^^

This specifies a list of 0 or more keys that should be specified in the
`Envault` request.

Each key specified here must be a key that is accessible by the provided
`apiKeyName`, and will result in an arbitrarily sized set of environment
variables and values to be returned by the service.

!!! tip

    The name of the keys specified here do not necessarily correspond to the
    names of the environment variables that are returned by the service.
    Rather, they specify a named set of variables; such as `auth` to return a
    set of variables that are used to authorize various services, for example.

    The same keys can be used in multiple configuration files, allowing you to
    easily share a common set of variables and values between projects.

## Example Config File

```yaml
apiKeyName: envault_dev_key
url: http://localhost:8787/
vars:
  - other
  - test/first
```
