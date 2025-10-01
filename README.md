# Radioactive-Beamline-Tuning-Plugins

This repository contains a collection of plugins for the integration of **Artificial Intelligence** into the workflows of radioactive ion beam tuning.
 
The plugins extend Badger with additional **environments** and **interfaces** to communicate with machines in a VSystem control network via API server. 

---

## Installation

Clone the repository into the Badger plugin root:

```
git clone https://github.com/slopezcaceres/radioactive-beamline-tuning-plugins.git
```

Make sure the environment variable BADGER_PLUGIN_ROOT points to this repository so Badger can automatically discover the plugins:

```
export BADGER_PLUGIN_ROOT=/path/to/badger-plugins
```
You can add this line to your .bashrc or .zshrc for convenience.

## Plugin Structure
The repository is organized into submodules:

```
badger-plugins/
├── environments/   # Custom optimization environments
│   └── sectionX/
└── interfaces/     # Hardware/software interface definitions
    └── sectionX/
```

Each plugin follows the Badger plugin specification and can be loaded automatically when BADGER_PLUGIN_ROOT is set.

## Usage

After installing and configuring, launch Badger as usual.

The plugins from this repository will be available in the GUI.

Network operator should allow access to server before running the optimization. 


## Documentation

For details on the Badger framework itself, see the official documentation:

Badger Optimizer (https://xopt-org.github.io/Badger/)

## Contributing

Contributions are welcome!

To add a new plugin:

Create a new folder under environments/ or interfaces/.

Follow the structure of existing plugins.

Submit a pull request.

