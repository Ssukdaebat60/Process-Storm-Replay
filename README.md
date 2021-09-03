# Process-Storm-Replay
It is a Python library to extract game event information from Heroes of the Storm replay files into .json.

* It extracts game events such as Nick_Name, Hero, Victory, Team_Id, and  Talent Choices.
(It is based on [heroprotocol](https://github.com/Blizzard/heroprotocol))


## Requirements
* Python 3.x

* Python Libraries & Packages:
  * myqy 0.2.5+
  * six 1.14.0+
  * heroprotocol


## Usage
 >user$  python3 ProcessStormReplay "replayfilename.StormReplay"
```bash
example:  python3 ProcessStormReplay "Tomb of the Spider Queen.StormReplay"
```


## About Versions
When heroes of the storm is updated, heroprotocol is also updated.
So you have to change heroprotocol library version every game update.

```python
example:  from heroprotocol.versions import protocol85894 as protocol --> from heroprotocol.versions import protocol90924 as protocol
```
protocol85894, 85894 is version.
