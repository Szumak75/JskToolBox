# NetAddressTool

The project contains sets of base classes for operations on IPv4 addresses.

## Public Classes

Octet

Address

Netmask

Network

SubNetwork

## Octet

The class for IPv4 octet representation.

### Public properties

```
value: int
```
Return ostet as integer.

### Public setters

```
value: Union[str, int Octet]
```
Set octet from integer, string or other octet object.

### Functional properties

The class has been equipped with comparators that allow comparing objects with each other.

Validation of the assigned value is also carried out, in the event of exceeding the allowable range, the ValueError exception is thrown.

