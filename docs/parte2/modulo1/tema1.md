# Tema 1: Introducción a Azure desde cero

### Descripción
**Azure** es la nube de Microsoft: un conjunto de servicios que usas por internet en lugar de comprar y mantener tus propios servidores. Pagas por lo que consumes, escalas cuando lo necesitas y delegas en Microsoft el hardware, la energía y gran parte de la seguridad física.

Analogía de Microsoft Learn: la nube de Microsoft es un **edificio de departamentos**. Tu **tenant** es tu departamento, con sus propias llaves y reglas. Dentro organizas tus cosas en cajones (**grupos de recursos**) y cada objeto es un **recurso**. La **suscripción** es el contrato de luz y agua: define quién paga y cuánto puedes consumir.

Este tema es la base de toda la Parte 2. Antes de crear un agente o un índice de búsqueda necesitas entender cuatro cosas:
- **Dónde vive cada cosa:** regiones, zonas, suscripciones y grupos de recursos.
- **Quién puede hacer qué:** Microsoft Entra ID, RBAC, identidades administradas y Key Vault.
- **Cómo se gobierna:** etiquetas, candados, políticas y nombres.
- **Cuánto cuesta:** presupuestos y análisis de costos.

Al final harás un **tutorial completo** en el que creas, proteges, revisas y borras un laboratorio real usando el portal, Cloud Shell, la CLI y Python.

> [!NOTE]
> Las imágenes de este tema vienen de la documentación oficial de Microsoft Learn y se cargan desde su sitio; cada una indica su fuente. El portal cambia seguido, así que lo que veas en pantalla puede variar un poco respecto a las capturas.

---

## 1. La nube y quién es responsable de qué

### 1.1 Qué cambia al usar la nube
- **Pago por uso:** en lugar de comprar servidores por adelantado, pagas cada mes lo que consumes. Si borras un recurso, en general deja de cobrarse (hay excepciones que verás en la [sección 6](#6-costos)).
- **Elasticidad:** escalas en minutos, ya sea **horizontalmente** (más instancias) o **verticalmente** (más CPU o RAM), y regresas cuando baja la demanda.
- **Alcance global:** despliegas en regiones de todo el mundo sin construir centros de datos.
- **Servicios administrados:** con PaaS, Microsoft se encarga de tareas como el sistema operativo y los parches.

### 1.2 IaaS, PaaS y SaaS
Siguiendo con la analogía del edificio, la diferencia está en cuánto del departamento te toca a ti:

| Modelo | Qué administras tú | Ejemplos de Microsoft | Analogía |
|---|---|---|---|
| **IaaS** (infraestructura como servicio) | Máquinas virtuales, sistema operativo y aplicaciones | Azure Virtual Machines, discos, redes virtuales | Rentas un departamento **vacío**: tú amueblas, pintas y arreglas |
| **PaaS** (plataforma como servicio) | Tu código, tus datos y la configuración | App Service, Azure Functions, Azure SQL Database, Azure Storage, **Microsoft Foundry** | Departamento **amueblado con mantenimiento**: solo traes tus cosas |
| **SaaS** (software como servicio) | Tus datos, usuarios y ajustes | Microsoft 365, Dynamics 365 | **Cuarto de hotel**: llegas y lo usas |

Microsoft Foundry es **PaaS**: Microsoft opera la infraestructura de los modelos y del servicio de agentes, y tú decides qué modelos despliegas, quién tiene acceso, qué datos conectas y cómo se configura la red.

### 1.3 Modelo de responsabilidad compartida
Mudarte a la nube no significa olvidarte de la seguridad. Significa **repartirla**.

![Diagrama del modelo de responsabilidad compartida entre el cliente y Microsoft en local, IaaS, PaaS y SaaS](https://learn.microsoft.com/en-us/azure/security/fundamentals/media/shared-responsibility/shared-responsibility.svg)

*Modelo de responsabilidad compartida. Arriba está lo que **siempre** es tuyo (información y datos, dispositivos, cuentas e identidades), en medio lo que **varía** según el modelo y abajo lo que **pasa al proveedor** en la nube (hosts, red y centro de datos físicos). Fuente: [Microsoft Learn – Shared responsibility in the cloud](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility).*

La misma página publica esta matriz (es más reciente que el diagrama y agrupa algunas filas distinto, pero el mensaje es igual):

| Área | Local | IaaS | PaaS | SaaS |
|---|---|---|---|---|
| Datos del cliente | Tú | Tú | Tú | Tú |
| Configuraciones y ajustes | Tú | Tú | Tú | Tú |
| Identidades y usuarios | Tú | Tú | Tú | Tú |
| Dispositivos cliente | Tú | Tú | Tú | Compartida |
| Aplicaciones | Tú | Tú | Compartida | Compartida |
| Controles de red | Tú | Tú | Compartida | Microsoft |
| Sistema operativo | Tú | Tú | Microsoft | Microsoft |
| Hosts, red y centro de datos físicos | Tú | Microsoft | Microsoft | Microsoft |

Lo más importante: **en cualquier modelo de nube, tus datos, tus cuentas y la gestión de accesos son tuyos**. Eso incluye RBAC, MFA y acceso condicional. Microsoft protege el centro de datos, pero no puede impedir que le des el rol Owner a quien no debe o que subas tu llave a GitHub. De eso tratan las secciones [4](#4-identidad-y-acceso-quién-eres-y-qué-puedes-hacer) y [5](#5-gobierno-etiquetas-candados-políticas-y-nombres).

### 1.4 Las cuatro categorías de servicios (y dónde encaja la IA)
- **Cómputo:** "rentar computadoras en la nube" que escalan cuando quieras (VMs, contenedores, funciones).
- **Almacenamiento:** archivos, bases de datos, imágenes, respaldos.
- **Redes:** conectar recursos entre sí, a internet o a tu organización de forma segura.
- **Servicios de aplicaciones:** plataformas listas para hospedar apps sin administrar servidores.

Una aplicación de IA real usa piezas de todas las categorías:

| Necesidad de tu app de IA | Servicios típicos en Azure |
|---|---|
| Ejecutar tu código (API, agente, interfaz web) | App Service, Azure Container Apps, Azure Functions, AKS, VMs |
| Guardar documentos y datos | Blob Storage, Azure SQL Database, Cosmos DB, Azure Database for PostgreSQL |
| Conectar de forma privada | Redes virtuales y *private endpoints* |
| Modelos, agentes, búsqueda y evaluación | **Microsoft Foundry**, Azure AI Search |
| Identidad y secretos | **Microsoft Entra ID**, **identidades administradas**, **Azure Key Vault** |

---

## 2. Infraestructura global: regiones y zonas de disponibilidad

### 2.1 Regiones
- Una **región** es la ubicación física de un conjunto de centros de datos (por ejemplo *East US 2*, *Sweden Central* o *Mexico Central*, que está en Querétaro).
- La eliges al crear casi cualquier recurso, y afecta varias cosas:
  - **Latencia:** qué tan rápido llegan las respuestas a tus usuarios.
  - **Cumplimiento:** dónde viven los datos.
  - **Disponibilidad:** no todos los servicios ni todos los modelos de IA están en todas las regiones.
  - **Precio:** puede variar entre regiones.
- Para ver las regiones disponibles para tu suscripción usa `az account list-locations -o table`.

**Pares de regiones.** Microsoft asocia algunas regiones con otra de la misma geografía para formar un **par**:
- **Recuperación ordenada:** si toda una geografía falla, una región de cada par se recupera primero.
- **Actualizaciones escalonadas:** las actualizaciones planeadas se aplican primero en una región del par y después en la otra.
- **Réplica:** algunos servicios replican al par automáticamente, por ejemplo el almacenamiento geo-redundante (GRS).

Muchas regiones nuevas **no tienen par** y usan zonas de disponibilidad como su principal mecanismo de redundancia.

| Región | Zonas de disponibilidad | Región par |
|---|---|---|
| Mexico Central | 3 | Sin par |
| Brazil South | 3 | South Central US |
| East US 2 | 4 (al menos una en versión preliminar) | Central US |
| West US 3 | 3 | East US (en un solo sentido) |
| Sweden Central | 3 | Sweden South (acceso restringido) |

> [!IMPORTANT]
> Desplegar en una región que tiene par **no** te da por sí solo alta disponibilidad, recuperación ante desastres ni conmutación por error. Eso lo diseñas tú.

### 2.2 Zonas de disponibilidad
Una **zona de disponibilidad** es un grupo de uno o más centros de datos dentro de una región, con **energía, enfriamiento y red independientes**. Si una zona falla, las demás siguen dando servicio.

![Diagrama de cuatro regiones de ejemplo: dos con tres zonas de disponibilidad y dos sin zonas](https://learn.microsoft.com/en-us/azure/reliability/media/availability-zones-overview/regions-availability-zones.svg)

*Las regiones 1 y 2 tienen tres zonas de disponibilidad, algunas con un centro de datos y otras con varios. Las regiones 3 y 4 no tienen zonas. Fuente: [Microsoft Learn – What are Azure availability zones?](https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview).*

Analogía: las zonas son como los **edificios separados de un mismo hospital**, cada uno con su propia planta de luz, su clima y sus conexiones. Si un edificio se queda sin luz, los otros siguen atendiendo. Pero si un huracán afecta a toda la ciudad (la región completa), el hospital entero sufre, y para eso existen las estrategias **multirregión**.

- **Distancia y latencia:**
  - Las zonas suelen estar separadas por varios kilómetros, normalmente a menos de 100 km entre sí.
  - Microsoft busca una latencia de ida y vuelta menor a ~2 ms entre zonas.
- **Costo:** Azure no cobra la transferencia de datos entre zonas de la misma región.
- **Tres formas de usarlas:**
  - **Redundante entre zonas:** el servicio replica o reparte tu recurso en varias zonas, y Microsoft hace la conmutación por error automáticamente.
  - **Zonal:** tú eliges la zona. Para sobrevivir a la caída de una zona necesitas varias instancias en zonas distintas y tu propio plan de conmutación.
  - **No zonal (regional):** Azure coloca el recurso en cualquier zona. Si esa zona cae, tu recurso podría caer con ella.
- **Límite:** las zonas **no protegen contra la caída de una región completa**.

![Diagrama de un recurso redundante entre zonas con una instancia en cada una de las tres zonas](https://learn.microsoft.com/en-us/azure/reliability/media/availability-zones-overview/zone-redundant.svg)

*Recurso redundante entre zonas: una instancia en cada zona y el servicio se encarga de repartir el tráfico y replicar. Fuente: [Microsoft Learn – What are Azure availability zones?](https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview).*

**Zonas lógicas vs. físicas.** La "zona 1" que ves en tu suscripción es un número **lógico**. Cada suscripción recibe su propio mapeo al crearse, así que tu zona 1 y la zona 1 de otra suscripción pueden ser edificios distintos.

![Diagrama: la zona física 1 corresponde a la zona lógica 2 en la suscripción A y a la zona lógica 3 en la suscripción B](https://learn.microsoft.com/en-us/azure/reliability/media/availability-zones-overview/availability-zones-logical-physical.svg)

*La misma zona física aparece con números lógicos distintos en dos suscripciones. Fuente: [Microsoft Learn – What are Azure availability zones?](https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview).*

Para ver el mapeo de tu suscripción en una región:
```bash
az account list-locations --query "[?name=='mexicocentral'].availabilityZoneMappings" -o json
```

### 2.3 Cómo elegir región para un proyecto de IA
1. **Residencia de datos y cumplimiento.** ¿Dónde deben vivir los datos según tu organización o regulación?
2. **Disponibilidad.** ¿Existen en esa región el servicio, el modelo y el tipo de despliegue que necesitas? Revisa la tabla de disponibilidad de modelos de Foundry antes de crear nada.
3. **Cuota.** Las cuotas de modelos (por ejemplo, tokens por minuto) se controlan a nivel de **suscripción**:
   - Con despliegues **Global Standard**, el mismo modelo comparte una sola bolsa de cuota entre todas las regiones.
   - Con **Data Zone Standard**, se comparte por zona de datos (por ejemplo, EE. UU. o la UE).
4. **Latencia** hacia tus usuarios y hacia tus otros servicios (base de datos, índice de búsqueda).
5. **Resiliencia.** ¿La región tiene zonas? ¿Necesitas una segunda región?
6. **Precio** del servicio en esa región.

En este acordeón usamos **East US 2** en los ejemplos.

---

## 3. Cómo se organiza Azure

### 3.1 La jerarquía, de arriba abajo
```
Tenant (Microsoft Entra ID: usuarios, grupos, políticas)
 └── Suscripción (facturación, cuotas, control de acceso)
      └── Grupo de recursos (carpeta lógica)
           └── Recursos (Foundry, Storage, Key Vault, AI Search...)
```
- **Tenant:** se crea cuando una organización se registra en Azure o Microsoft 365. Cada tenant está aislado.
- **Suscripción:** liga el uso a un medio de pago (o créditos). Un tenant puede tener varias (ej. *Dev* y *Prod*).
- **Grupo de recursos:** agrupa recursos con el mismo ciclo de vida. Si borras el grupo, borras todo lo que contiene (útil para limpiar laboratorios).
- **Recurso:** tiene un **tipo** (ej. `Microsoft.CognitiveServices/accounts` para Foundry, `Microsoft.Storage/storageAccounts` para almacenamiento), nombre, ID, **región**, **nivel de precio** y permisos.

Azure Resource Manager define **cuatro niveles de ámbito** (*scope*). Lo que asignas en un nivel, como permisos o políticas, **se hereda hacia abajo**:

![Los cuatro niveles de ámbito de Azure: grupos de administración, suscripciones, grupos de recursos y recursos](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/media/overview/scope-levels.png)

*Grupos de administración → suscripciones → grupos de recursos → recursos. Fuente: [Microsoft Learn – What is Azure Resource Manager?](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview).*

El tenant no aparece en ese diagrama porque no es uno de estos niveles: es el **directorio de identidades** (Microsoft Entra ID) en el que confían todas tus suscripciones. La raíz de la jerarquía de grupos de administración lleva justamente el nombre de *Tenant Root Group*.

### 3.2 Azure Resource Manager: la puerta de entrada
Toda petición para crear, cambiar o borrar recursos pasa por **Azure Resource Manager (ARM)**, sin importar desde dónde la hagas:

![Azure Resource Manager recibe las peticiones del portal, PowerShell, la CLI, los SDK y clientes REST, las autentica y las reenvía a cada servicio](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/media/overview/consistent-management-layer.png)

*El portal, PowerShell, la CLI, los SDK y los clientes REST llegan al mismo Resource Manager, que autentica y autoriza la petición antes de pasarla al servicio. Fuente: [Microsoft Learn – What is Azure Resource Manager?](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview).*

Analogía: ARM es la **recepción del edificio**. No importa si llegas caminando (portal) o mandas a un mensajero (CLI, SDK): todos pasan por el mismo mostrador. Ahí revisan tu identificación (**autenticación**) y tu lista de accesos (**RBAC**) antes de dejarte pasar al servicio correspondiente.

Consecuencias prácticas:
- **Resultados consistentes:** todo lo que haces en el portal también se puede hacer con PowerShell, la CLI, REST o los SDK. Las funciones nuevas de las APIs llegan al portal en un máximo de 180 días.
- **Infraestructura declarativa:** con **plantillas ARM** (JSON) o **Bicep** describes *qué* quieres y ARM se encarga de *cómo* crearlo, de forma repetible.

### 3.3 Proveedores de recursos, tipos e IDs
- Un **proveedor de recursos** es el conjunto de operaciones REST de un servicio. Por ejemplo, Key Vault es el proveedor `Microsoft.KeyVault`.
- El **tipo de recurso** sigue el formato `{proveedor}/{tipo}`, como `Microsoft.KeyVault/vaults`. Los recursos hijos agregan niveles: `Microsoft.CognitiveServices/accounts/projects`.

| Lo que usarás en este curso | Tipo de recurso | Abreviatura CAF |
|---|---|---|
| Grupo de recursos | `Microsoft.Resources/resourceGroups` | `rg` |
| Recurso de Foundry | `Microsoft.CognitiveServices/accounts` (kind `AIServices`) | `aif` |
| Proyecto de Foundry | `Microsoft.CognitiveServices/accounts/projects` | `proj` |
| Azure AI Search | `Microsoft.Search/searchServices` | `srch` |
| Key Vault | `Microsoft.KeyVault/vaults` | `kv` |
| Identidad administrada | `Microsoft.ManagedIdentity/userAssignedIdentities` | `id` |
| Cuenta de almacenamiento | `Microsoft.Storage/storageAccounts` | `st` |
| Log Analytics / Application Insights | `Microsoft.OperationalInsights/workspaces` / `Microsoft.Insights/components` | `log` / `appi` |

**Registro de proveedores.** Tu suscripción debe estar **registrada** en un proveedor antes de usarlo:
- Algunos proveedores vienen registrados de fábrica.
- El portal y las plantillas suelen registrar los que necesitan por ti.
- Registrar requiere la operación `*/register/action`, que incluyen los roles **Contributor** y **Owner**.
- Microsoft recomienda registrar **solo lo que vas a usar**: cada proveedor registrado agrega una aplicación a tu tenant.
- No puedes "desregistrar" un proveedor mientras tengas recursos suyos.

**El ID de un recurso** dice exactamente dónde vive:
```
/subscriptions/<id-de-suscripción>
  /resourceGroups/rg-acordeon-ai901
    /providers/Microsoft.CognitiveServices/accounts/aif-acordeon-jj
      /projects/proj-acordeon
```
Cada prefijo del ID es un **ámbito** en el que puedes asignar permisos, y lo que asignas en un prefijo aplica a todo lo que cuelga de él. Foundry lleva esto un nivel más abajo: puedes asignar un rol a un agente individual con un ID que termina en `/projects/<proyecto>/agents/<agente>`. En la [práctica 8.1](#81-anatomía-de-un-id-y-herencia-de-permisos-alcancespy) lo verás funcionar.

### 3.4 Plano de control vs. plano de datos
Esta distinción explica la mayoría de los errores de permisos que vas a encontrar:

| | Plano de control | Plano de datos |
|---|---|---|
| Para qué sirve | Crear, configurar y borrar recursos | Usar lo que el recurso ofrece |
| A dónde va la petición | `management.azure.com` (ARM) | Al endpoint del servicio: `<bóveda>.vault.azure.net`, `<recurso>.services.ai.azure.com` |
| En Foundry | Crear el recurso o un proyecto, desplegar modelos, crear conexiones, asignar roles, rotar llaves, configurar Private Link | Inferencia (chat, embeddings), construir agentes, evaluaciones, *fine-tuning* |
| En Key Vault | Crear la bóveda, cambiar sus etiquetas o su red | Crear, leer y borrar secretos, llaves y certificados |
| Permisos RBAC | `actions` | `dataActions` |
| ¿Lo bloquea un candado? | Sí | No |

![Alex, con el rol Owner, tiene acceso al plano de control; Jay, con Foundry Owner, tiene acceso a control y datos del recurso de Foundry](https://learn.microsoft.com/en-us/azure/foundry/media/authentication-authorization/foundry-rbac-control-data-separation.png)

*La línea punteada separa control (arriba) de datos (abajo). Alex es **Owner** de la suscripción: administra todo, incluso conexiones y despliegues de modelos, pero **no** entra a agentes, evaluaciones ni APIs de datos. Jay es **Foundry Owner**: cubre el recurso de Foundry en ambos planos. Fuente: [Microsoft Learn – Authentication and authorization in Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/concepts/authentication-authorization-foundry).*

Analogía: el **plano de control** es la administración del edificio (dar de alta departamentos, cambiar cerraduras). El **plano de datos** es lo que haces dentro del departamento (abrir la caja fuerte). El administrador del edificio puede cambiar cerraduras, pero eso **no** le da la combinación de tu caja fuerte: para eso necesita un rol de datos.

### 3.5 Grupos de administración
Cuando una organización tiene muchas suscripciones, las agrupa en **grupos de administración** para aplicarles políticas y permisos una sola vez:

![Jerarquía de ejemplo: Tenant root group, Contoso y grupos Platform, Landing zones, Decommissioned y Sandbox con sus suscripciones](https://learn.microsoft.com/en-us/azure/governance/media/mg-org.png)

*Jerarquía típica: de la raíz cuelgan grupos de plataforma (seguridad, identidad, conectividad), "zonas de aterrizaje" para las cargas de trabajo, un grupo para lo que se va a retirar y otro de *sandbox* para experimentar. Fuente: [Microsoft Learn – What are Azure management groups?](https://learn.microsoft.com/en-us/azure/governance/management-groups/overview).*

- La raíz se llama **Tenant Root Group** y su ID es el ID del tenant.
- Admite hasta **6 niveles** de profundidad (sin contar la raíz ni el nivel de suscripción) y hasta **10,000** grupos por directorio.
- Lo que asignas a un grupo de administración (RBAC, Azure Policy) lo **heredan** todas sus suscripciones.

Con una cuenta personal o de estudiante tendrás una sola suscripción y no los necesitas, pero en empresas son la norma.

### 3.6 Suscripciones y tipos de cuenta
Una **suscripción** cumple tres funciones:
- **Frontera de facturación:** todo lo que creas en ella se cobra a su medio de pago o crédito.
- **Frontera de acceso:** quien es Owner de la suscripción controla todo lo que contiene.
- **Frontera de límites:** las cuotas, incluidas las de modelos de IA, se cuentan por suscripción.

Por eso las empresas separan *Dev*, *Test* y *Prod* en suscripciones distintas.

Formas de conseguir una:

| Opción | Qué incluye | Requisitos | Al terminar |
|---|---|---|---|
| **Cuenta gratuita** (clientes nuevos) | USD 200 de crédito durante 30 días, más de 20 servicios gratis cada mes por 12 meses y más de 65 servicios siempre gratuitos | Teléfono y tarjeta de crédito o débito (no de prepago); puede aparecer una retención temporal de verificación de USD 1 | Debes pasar a **pago por uso**; si no, la cuenta se deshabilita |
| **Azure for Students** | USD 100 de crédito por 12 meses | Ser estudiante universitario de tiempo completo; **sin tarjeta** | Se renueva cada año mientras sigas siendo estudiante; si no, pasas a pago por uso o se deshabilita |
| **Pago por uso** | Pagas lo que consumes | Medio de pago | **No tiene tope de gasto**: por eso existen los presupuestos ([sección 6](#6-costos)) |
| **Suscripción de tu empresa o escuela** | Lo que te asigne tu organización | Una cuenta de la organización | Pregunta qué rol tienes: el tutorial necesita **Owner** |

### 3.7 Grupos de recursos a fondo
- Todos los recursos de un grupo deberían compartir el **mismo ciclo de vida**: se crean, actualizan y borran juntos.
- Un recurso pertenece a **un solo** grupo, aunque puedes **moverlo** a otro.
- Un recurso puede conectarse a recursos de otros grupos. Por ejemplo, una web app puede usar una base de datos que vive en otro grupo.
- La **región del grupo** indica dónde se guardan sus **metadatos**, lo que importa para cumplimiento. Los recursos pueden estar en otras regiones, aunque Microsoft recomienda usar la misma.
- **Borrar el grupo borra todo lo que contiene.**
- Límite: hasta **800 instancias de un mismo tipo** de recurso por grupo, con algunas excepciones.

Regla práctica: un grupo por aplicación y entorno (`rg-<carga>-<entorno>`), y un grupo por laboratorio, para poder borrarlo completo al terminar.

---

## 4. Identidad y acceso: quién eres y qué puedes hacer

### 4.1 Microsoft Entra ID: autenticación
- **Microsoft Entra ID** (antes Azure Active Directory) es el servicio de identidad. Tu **tenant** es la instancia de Entra ID de tu organización.
- **Autenticación** es demostrar quién eres: contraseña y MFA, y a cambio recibes un **token**. **Autorización** es decidir qué puedes hacer con ese token, y de eso se encarga **RBAC**.
- Hay cuatro tipos de **entidad de seguridad** (*security principal*) a las que puedes dar permisos:
  - **Usuario:** una persona.
  - **Grupo:** un conjunto de usuarios.
  - **Entidad de servicio** (*service principal*): la identidad de una aplicación.
  - **Identidad administrada:** una entidad de servicio que Azure administra por ti ([4.5](#45-identidades-administradas)).

Analogía: Entra ID es la **credencial con foto** que te dan en la recepción del edificio. RBAC es la **lista** que dice a qué pisos y cuartos abre esa credencial.

### 4.2 Azure RBAC: autorización
Una **asignación de rol** une tres piezas: **quién** (entidad de seguridad) + **qué puede hacer** (definición de rol) + **dónde** (ámbito).

![Una asignación de rol combina entidad de seguridad, definición de rol y ámbito: el grupo Marketing recibe Contributor sobre el grupo de recursos pharma-sales](https://learn.microsoft.com/en-us/azure/role-based-access-control/media/overview/rbac-overview.png)

*Ejemplo oficial: el grupo **Marketing** (quién) recibe **Contributor** (qué) en el grupo de recursos **pharma-sales** (dónde). Observa el JSON del rol: `Actions: ["*"]` con `NotActions` que excluyen escribir y borrar en `Authorization`. Fuente: [Microsoft Learn – What is Azure RBAC?](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview).*

Una **definición de rol** es una lista de operaciones permitidas:
- `Actions` / `NotActions` para el plano de control.
- `DataActions` / `NotDataActions` para el plano de datos.

Estos son los roles generales más usados, tal como los publica Microsoft:

| Rol | `Actions` | `DataActions` | En una frase |
|---|---|---|---|
| **Owner** | `*` | ninguna | Control total, **incluido asignar roles** |
| **Contributor** | `*`, menos escribir/borrar en `Microsoft.Authorization` (y otras excepciones) | ninguna | Crea y administra todo, pero **no asigna roles** ni crea candados |
| **Reader** | `*/read` | ninguna | Solo ver |
| **User Access Administrator** | `*/read`, `Microsoft.Authorization/*` | ninguna | Administra accesos (y candados) |
| **Role Based Access Control Administrator** | `*/read`, escribir y borrar asignaciones de rol | ninguna | Solo asigna roles |

> [!IMPORTANT]
> **Owner no significa acceso a los datos.** Ninguno de los roles generales tiene `DataActions`. Por eso un Owner recibe *"The operation is not allowed by RBAC"* al leer secretos de una bóveda con RBAC ([4.6](#46-azure-key-vault)), y **no puede construir agentes** en Foundry ([4.3](#43-roles-de-microsoft-foundry)) hasta que se asigne un rol de datos.

Reglas que conviene memorizar:
- **Herencia:** lo asignado en un ámbito aplica a todo lo que está debajo. Nunca al revés: un rol en un proyecto no da nada sobre el recurso padre.
- **Modelo aditivo:** tus permisos efectivos son la **suma** de todas tus asignaciones.

  ![Un usuario con Contributor en la suscripción y Reader en un grupo de recursos termina con Contributor en ambos](https://learn.microsoft.com/en-us/azure/role-based-access-control/media/overview/rbac-multiple-roles.png)

  *Contributor en la suscripción + Reader en un grupo = Contributor también en ese grupo: el permiso más amplio ya llega por herencia. Fuente: [Microsoft Learn – What is Azure RBAC?](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview).*
- **Grupos transitivos:** si estás en un grupo que está dentro de otro grupo con un rol, ese rol también es tuyo. Asigna roles a **grupos**, no a personas sueltas.
- **Primero se revisan las denegaciones:** si una *asignación de denegación* aplica, el acceso se bloquea aunque tengas un rol que lo permita.

  ![Flujo de evaluación de Azure RBAC: primero asignaciones de denegación, luego asignaciones de rol y condiciones](https://learn.microsoft.com/en-us/azure/role-based-access-control/media/overview/evaluation-logic.png)

  *Cómo decide ARM: parte de "sin acceso", junta las asignaciones que aplican, evalúa primero las denegaciones y después busca un rol que coincida con quién, qué acción y qué ámbito (más sus condiciones, si las hay). Fuente: [Microsoft Learn – What is Azure RBAC?](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview).*
- **Alcance global y propagación:** las asignaciones se guardan globalmente (sirven en cualquier región), pero tardan **unos minutos** en propagarse. Si acabas de asignar un rol y sigue fallando, espera un poco.
- **Mínimo privilegio:** da el rol más pequeño, en el ámbito más pequeño, que permita hacer el trabajo.

### 4.3 Roles de Microsoft Foundry
Foundry tiene roles propios porque los generales no cubren el plano de datos:

| Rol | Construir en un proyecto (agentes, evaluaciones) | Crear recursos de Foundry | Administrar modelos | Asignar roles | Publicar agentes |
|---|---|---|---|---|---|
| **Foundry User** | ✔ | ✘ | ✘ | ✘ | ✘ |
| **Foundry Project Manager** | ✔ | ✘ | ✘ | Solo Foundry User | ✔ |
| **Foundry Account Owner** | ✘ | ✔ | ✔ | Foundry User, ACR y monitoreo | ✘ |
| **Foundry Owner** | ✔ | ✔ | ✔ | Foundry User, ACR y monitoreo | ✔ |
| **Foundry Agent Consumer** | ✘ (solo usa los endpoints de los agentes) | ✘ | ✘ | ✘ | ✘ |
| Owner (Azure) | ✘ | ✔ | ✔ | Cualquier rol | ✔ |
| Contributor (Azure) | ✘ | ✔ | ✔ | ✘ | ✘ |
| Reader (Azure) | ✘ | ✘ | ✘ | ✘ | ✘ |

![Cinco personas y su alcance: Alex (Owner), Jay (Foundry Owner), Ben (Foundry Account Owner), Claire (Foundry Project Manager) y Dylan (Foundry User)](https://learn.microsoft.com/en-us/azure/foundry/media/authentication-authorization/role-mapping-diagram.png)

*Cada recuadro de color es el alcance de un rol:*
- *Alex (**Owner**) cubre todo el plano de control, pero nada del de datos.*
- *Ben (**Foundry Account Owner**) administra el recurso y sus despliegues, sin entrar a los datos.*
- *Claire (**Foundry Project Manager**) trabaja dentro de los proyectos.*
- *Dylan (**Foundry User**) vive en el plano de datos: agentes, evaluaciones y APIs de OpenAI.*
- *Jay (**Foundry Owner**) cubre ambos planos.*

*Fuente: [Microsoft Learn – Authentication and authorization in Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/concepts/authentication-authorization-foundry).*

Lo que necesitas saber para trabajar:
- **Nombres nuevos:** los roles se llamaban *Azure AI User*, *Azure AI Owner*, *Azure AI Account Owner* y *Azure AI Project Manager*. Puedes ver ambos nombres mientras termina el cambio.
- **En scripts usa el ID del rol (GUID)**, no el nombre. Por ejemplo, Foundry User es `53ca6127-db72-4b80-b1b0-d745d6d5456d`.
- **Mínimo para empezar:** asigna **Foundry User** sobre el recurso de Foundry a **tu usuario** y a la **identidad administrada del proyecto**.
  - Si creas el proyecto desde el **portal** y puedes asignar roles, ambas asignaciones se hacen solas.
  - **Desde la CLI o el SDK no se hacen**, y por eso el [Paso 8](#paso-8-asigna-los-roles-de-foundry) del tutorial las crea a mano.
- **Patrón empresarial:** los desarrolladores reciben *Foundry User* en el proyecto y *Reader* en el recurso. Quien solo conversa con agentes recibe *Foundry Agent Consumer*.
- **Roles que no debes usar para Foundry:**
  - Los que empiezan con *Cognitive Services*. La excepción es *Cognitive Services Usages Reader*, que se asigna en la suscripción para ver cuotas.
  - *Azure AI Developer*: sirve para hubs y Azure Machine Learning, no para proyectos de Foundry.

### 4.4 Llaves (API keys) vs. Microsoft Entra ID
Foundry acepta dos formas de autenticación, y la diferencia es de seguridad, no de comodidad:
- **Una llave da acceso completo al recurso.** No se puede limitar a ciertos usuarios o acciones, no dice *quién* hizo cada llamada y RBAC no aplica. Sirve para prototipos rápidos; si la usas, rótala con frecuencia y nunca la subas a un repositorio.
- **Microsoft Entra ID** da RBAC de mínimo privilegio, auditoría por identidad, acceso condicional e identidades administradas. Microsoft lo recomienda para producción. La comparación detallada está en el [Tema 3](tema3.md#autenticación-llave-vs-entra-id).
- **Detalle que sorprende:** el rol *Foundry User* incluye la acción `Microsoft.CognitiveServices/accounts/listkeys/action`. Quien tenga ese rol puede leer la llave y, con ella, saltarse RBAC. Por eso Microsoft sugiere quitar la autenticación por llave cuando todos tus clientes ya usen tokens; puedes desactivar la autenticación local desde tus plantillas de despliegue.
- **El subdominio personalizado es obligatorio para tokens:** la autenticación con Entra ID usa el endpoint `https://<recurso>.services.ai.azure.com`, que requiere un subdominio propio. Por eso el comando de creación del tutorial lleva `--custom-domain`.

### 4.5 Identidades administradas
Una **identidad administrada** es una identidad de Entra ID que Azure le asigna a un recurso de cómputo (VM, App Service, Container Apps, Functions, AKS…) para que tu código obtenga tokens **sin contraseñas ni llaves**. Tú nunca ves sus credenciales y su uso no tiene costo adicional.

| | Asignada por el sistema | Asignada por el usuario |
|---|---|---|
| Ciclo de vida | Nace y muere con el recurso | Independiente: hay que borrarla explícitamente |
| ¿Se comparte? | No, pertenece a un solo recurso | Sí, puedes asignarla a varios recursos |
| Recomendación de Microsoft | — | **Recomendada** para los servicios de Microsoft |

Cómo la usa una app, en cuatro pasos:
1. **Creas** la identidad, o activas la del sistema en tu servicio.
2. **La asignas** al servicio que ejecuta tu código.
3. **Le das un rol** sobre el recurso destino, por ejemplo *Key Vault Secrets User* o *Foundry User*.
4. **Tu código** usa `DefaultAzureCredential`, que en tu PC toma tu sesión de `az login` y dentro de Azure toma la identidad administrada **sin cambiar una línea**.

Foundry también las usa por dentro. El recurso y cada proyecto tienen su propia identidad (la CLI crea la del recurso con `--assign-identity` y la del proyecto por defecto). Por ejemplo, para que Foundry lea una cuenta de almacenamiento nueva le das a la identidad del recurso el rol *Storage Blob Data Reader* en esa cuenta.

Analogía: la identidad administrada es el **gafete de empleado** que el edificio le da a tu app. No tiene contraseña que se pueda perder ni anotar en un papel. El gafete del sistema se destruye cuando el empleado se va; el de usuario lo puedes reasignar a otro empleado.

### 4.6 Azure Key Vault
**Azure Key Vault** es la caja fuerte para **secretos** (API keys, cadenas de conexión, contraseñas), **llaves** criptográficas y **certificados**.
- **Dos planos:**
  - **Control:** crear la bóveda, cambiar sus etiquetas o su red, en `management.azure.com`.
  - **Datos:** leer y escribir secretos, en `https://<bóveda>.vault.azure.net`.
- **Modelo de permisos:** puede ser **Azure RBAC** o las **políticas de acceso** heredadas. A partir de la API `2026-02-01`, **RBAC es el modelo predeterminado** para las bóvedas nuevas.
- **Riesgo de las políticas de acceso:** con ellas, alguien con *Contributor* en la bóveda puede darse acceso a los datos editando la política. Con RBAC necesita un rol de datos explícito.

![Pestaña Access configuration al crear una bóveda: el modelo de permisos Azure role-based access control aparece marcado como recomendado](https://learn.microsoft.com/en-us/azure/key-vault/media/rbac/new-vault.png)

*Al crear una bóveda en el portal, la pestaña **Access configuration** ofrece "Azure role-based access control (recommended)" o "Vault access policy". Fuente: [Microsoft Learn – Azure RBAC para Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide).*

| Rol | Qué permite |
|---|---|
| **Key Vault Administrator** | Todo en el plano de datos (secretos, llaves, certificados); no administra la bóveda ni asigna roles |
| **Key Vault Secrets Officer** | Cualquier acción sobre los secretos, salvo administrar permisos |
| **Key Vault Secrets User** | Leer el contenido de los secretos (lo ideal para una app) |
| **Key Vault Reader** | Ver metadatos, pero **no** el valor de los secretos |
| **Key Vault Contributor** | Administrar bóvedas (plano de control); **no** da acceso a secretos |
| **Key Vault Purge Operator** | Purgar bóvedas eliminadas |

Buenas prácticas y reglas:
- **Una bóveda por aplicación y por entorno** (dev, pre-producción, producción), con los roles asignados en el ámbito de la bóveda.
- **Eliminación temporal** (*soft delete*):
  - Está siempre activa y no se puede apagar.
  - Una bóveda borrada se conserva de **7 a 90 días** (90 por defecto). Ese plazo se fija al crearla y luego no se puede cambiar.
  - Mientras dure el plazo **no puedes reutilizar el nombre**, salvo que la purgues.
- **Protección de purga:**
  - Es opcional e **irreversible**.
  - Con ella activa, nadie puede purgar la bóveda ni sus secretos hasta que termine el plazo. Actívala en producción; en un laboratorio te impide liberar el nombre.
- **Purgar una bóveda completa** solo lo puede hacer el Owner de la suscripción o alguien con *Key Vault Purge Operator*.
- **Costos:** Key Vault cobra por operaciones. Mientras algo está eliminado no genera uso; solo "purgar" y "recuperar" cuentan como operaciones.

---

## 5. Gobierno: etiquetas, candados, políticas y nombres
Cuatro herramientas que se confunden fácilmente:

| Herramienta | Pregunta que responde | Analogía del edificio |
|---|---|---|
| **RBAC** | ¿*Quién* puede hacer qué, y dónde? | La lista de qué llaves tiene cada quien |
| **Azure Policy** | ¿*Qué* configuraciones están permitidas, sin importar quién las haga? | El reglamento del condominio: nadie pinta la fachada de rojo, tenga la llave que tenga |
| **Candado** (*lock*) | ¿Se puede borrar o modificar esto? | Un sello de "no demoler" en la puerta |
| **Etiqueta** (*tag*) | ¿De quién es esto, para qué es y a quién se le cobra? | La etiqueta en cada caja de la mudanza |

### 5.1 Etiquetas
- Son pares **nombre=valor** (`entorno=lab`, `proyecto=acordeon-ai901`, `responsable=jj`) en recursos, grupos y suscripciones.
- **Para qué sirven:** filtrar en el análisis de costos, saber de quién es cada cosa y automatizar (por ejemplo, apagar todo lo que tenga `entorno=lab`).
- **Límites:**
  - Máximo **50** etiquetas por recurso.
  - Nombre de hasta **512** caracteres (128 en cuentas de almacenamiento) y valor de hasta **256**.
  - El nombre no admite `< > % & \ ? /`.
- **No se heredan:** etiquetar el grupo de recursos **no** etiqueta lo que tiene dentro. Para propagarlas usa Azure Policy. Lo comprobarás en el [Paso 12](#paso-12-etiquetas-agrega-consulta-y-comprueba-que-no-se-heredan).
- **Mayúsculas:** los nombres no distinguen entre mayúsculas y minúsculas; los valores **sí**.
- Se guardan en **texto plano** y aparecen en reportes de costos, historiales y plantillas exportadas. **Nunca pongas secretos en etiquetas.**
- Foundry agrega por su cuenta una etiqueta `project` al **consumo** de cada proyecto, así que puedes ver el gasto por proyecto sin etiquetar nada ([6.3](#63-análisis-de-costos)).

### 5.2 Candados (resource locks)
- **Dos tipos:**
  - **CanNotDelete** (en el portal, *Delete*): se puede leer y modificar, pero **no borrar**.
  - **ReadOnly** (*Read-only*): solo leer. Es como si todos, incluido el Owner, tuvieran únicamente el rol Reader.
- **Aplican a todos:** a diferencia de RBAC, un candado restringe a **todos los usuarios y roles**, Owner incluido.
- **Se heredan:** un candado en el grupo de recursos protege todo lo que contiene, incluso lo que agregues después. Si hay varios, gana el más restrictivo.
- **Solo afectan al plano de control:** un candado ReadOnly en un servidor SQL impide borrarlo o reconfigurarlo, pero no impide leer o escribir datos en sus bases.
- **Efectos inesperados de ReadOnly:** bloquea operaciones POST como **listar las llaves** de una cuenta de almacenamiento o arrancar una VM, y también la asignación de roles en esa cuenta.
- **Quién los crea o borra:** se necesita `Microsoft.Authorization/locks/*`, que tienen **Owner** y **User Access Administrator**. *Contributor* no puede.

En el portal: abre el recurso o grupo → **Settings › Locks** → **Add**.

![Pantalla Locks de un recurso sin candados, con el botón Add resaltado](https://learn.microsoft.com/en-us/azure/includes/media/resource-manager-lock-resources/add-lock.png)

![Formulario Add lock con nombre DatabaseServerLock, tipo Delete y una nota](https://learn.microsoft.com/en-us/azure/includes/media/resource-manager-lock-resources/set-lock.png)

*Se elige el nombre, el tipo (**Delete** o **Read-only**) y una nota que explique por qué existe. Fuente: [Microsoft Learn – Lock your resources](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources).*

### 5.3 Azure Policy
- Evalúa tus recursos contra **reglas del negocio** y puede bloquear lo que no cumpla.
- La diferencia con RBAC:
  - RBAC controla las **acciones del usuario** según quién es.
  - Policy controla el **estado del recurso**, sin importar quién hizo el cambio.
  - Aunque tengas permiso para crear algo, si el resultado no cumple la política, **la creación se bloquea**.
- **Políticas integradas típicas:**
  - **Allowed locations** (*Deny*): solo permite crear recursos en ciertas regiones. Útil para residencia de datos.
  - **Allowed resource types** (*Deny*): solo permite ciertos tipos de recurso.
  - **Add a tag to resources** (*Modify*): agrega una etiqueta obligatoria con un valor por defecto.
- **Efectos:** `audit`/`auditIfNotExists` (solo reportan), `deny`, `modify`, `deployIfNotExists` y `DenyAction`. Microsoft recomienda **empezar con `audit`** para medir el impacto antes de bloquear.
- Si al crear algo ves `RequestDisallowedByPolicy`, una política lo prohibió. Pregunta cuál y elige una región o configuración permitida.

### 5.4 Convención de nombres
El **Cloud Adoption Framework (CAF)** recomienda armar los nombres con piezas fijas, separadas por guiones cuando el recurso lo permite:

`<tipo>-<carga o proyecto>-<entorno>-<región>-<instancia>` → `rg-acordeon-ai901`, `aif-acordeon-dev`, `vm-sql-test-001`

Pero cada tipo de recurso tiene sus **propias reglas**:

| Recurso | Ámbito de unicidad | Longitud | Caracteres válidos |
|---|---|---|---|
| Grupo de recursos | Suscripción | 1-90 | Letras, dígitos, `_` `.` `(` `)` `-`; no termina en punto |
| Recurso de Foundry | Grupo de recursos (su **subdominio** es único en todo Azure) | 2-64 | Alfanuméricos y guiones; empieza y termina con alfanumérico |
| Key Vault | **Todo Azure** | 3-24 | Alfanuméricos y guiones; empieza con letra, termina con letra o número, sin guiones seguidos |
| Secreto de Key Vault | Bóveda | 1-127 | Alfanuméricos y guiones (**sin** guion bajo) |
| Identidad administrada | Grupo de recursos | 3-128 | Alfanuméricos, `-` y `_`; empieza con letra o número |
| Cuenta de almacenamiento | **Todo Azure** | 3-24 | Solo minúsculas y números (sin guiones) |
| Candado | Ámbito donde se asigna | 1-90 | Alfanuméricos, `.` `_` `-` `(` `)`; no termina en punto |

- Los nombres de recursos y grupos **no distinguen mayúsculas**, así que compáralos siempre sin distinguirlas.
- Los nombres "globales" (Key Vault, almacenamiento, subdominios) forman parte de una **URL pública**: si alguien en el mundo ya lo usa, no puedes usarlo tú. Por eso agregamos tus iniciales.

---

## 6. Costos

### 6.1 Cómo se cobra
- **Pagas por lo que usas.** Con un recurso de Foundry pagas los servicios que consumes (modelos de OpenAI, Speech, Content Safety, Vision, Document Intelligence, Language…), y cada uno tiene su propio medidor: tokens, transacciones, horas.
- **Dos modalidades:**
  - **Pago por uso**, según tu consumo de cada servicio.
  - **Niveles de compromiso**: una tarifa fija por cierta capacidad, más un excedente si la superas.
- **Lo que cobra aunque no lo uses:**
  - Los **despliegues provisionados** siguen cobrándose en un recurso de Foundry eliminado **hasta que lo purgues**. Borra los despliegues antes de borrar el recurso.
  - Los modelos con **fine-tuning** desplegados cobran hospedaje **por hora**, aunque nadie los llame.
- **Otros servicios del laboratorio:**
  - **Key Vault** cobra por operaciones.
  - Las **identidades administradas** no tienen costo adicional.
  - **Cloud Shell** no cobra por la sesión, pero sí por la cuenta de almacenamiento si eliges guardar archivos.
- **No hay "freno de mano":** Azure OpenAI no ofrece un límite duro de gasto. Un presupuesto **avisa**, pero no detiene nada. Para reaccionar en automático, el presupuesto puede disparar un **grupo de acciones** (por ejemplo, una función que apague recursos), y eso requiere desarrollo propio.
- Para estimar antes de crear, usa la [calculadora de precios de Azure](https://azure.microsoft.com/pricing/calculator/).

### 6.2 Presupuestos y alertas
Un **presupuesto** compara tu gasto contra un monto y manda alertas cuando cruzas umbrales. Microsoft recomienda crearlos para cada suscripción y grupo de recursos.

![Formulario para crear un presupuesto mensual: alcance, nombre, periodo de reinicio, fechas y monto, junto a una gráfica de costo real y pronóstico](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/media/tutorial-acm-create-budgets/create-monthly-budget.png)

*Paso 1 del asistente: **alcance**, **nombre**, **periodo de reinicio** (mensual, trimestral o anual), fechas y **monto**. A la derecha, el costo de meses anteriores (verde fuerte), el pronóstico (verde claro) y la línea roja del presupuesto. Fuente: [Microsoft Learn – Tutorial: Create and manage budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets).*

![Configuración de alertas: una alerta real al 90 % y una pronosticada al 100 %, con destinatarios de correo](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/media/tutorial-acm-create-budgets/budget-set-alert.png)

*Paso 2: condiciones de alerta. **Actual** (gasto real) al 90 % y **Forecasted** (pronóstico) al 100 %, más los correos que las recibirán. La propia pantalla sugiere agregar `azure-noreply@microsoft.com` a tus remitentes seguros para que las alertas no caigan en spam. Fuente: [Microsoft Learn – Tutorial: Create and manage budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets).*

Lo que tienes que saber de los presupuestos:
- **Solo avisan:** los recursos no se afectan y el consumo **no se detiene**.
- **No son en tiempo real:**
  - Los datos de costo suelen estar disponibles **entre 8 y 24 horas** después.
  - El presupuesto se evalúa **cada 24 horas**.
- **Alertas:**
  - Las hay sobre el gasto **real** o sobre el **pronóstico**. La de pronóstico te avisa *antes* de pasarte.
  - Cada presupuesto necesita al menos un umbral y un correo, y admite hasta **5 umbrales** y **5 correos**.
- **Grupos de acciones:** solo están disponibles en presupuestos de **suscripción** o **grupo de recursos**. Sirven para mandar notificaciones *push* o disparar automatizaciones.
- **Permisos:** para crear presupuestos necesitas **Contributor** o **Cost Management Contributor**.

### 6.3 Análisis de costos
**Cost Management › Cost analysis** muestra cuánto llevas gastado, el pronóstico y en qué se va el dinero:

![Análisis de costos acumulados del mes con línea de presupuesto, pronóstico y gráficas por servicio, ubicación y cuenta](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/media/tutorial-acm-create-budgets/cost-analysis.png)

*Costo acumulado del mes (verde), pronóstico (verde claro) y presupuesto (línea punteada roja). Abajo, el gasto agrupado por servicio, ubicación y cuenta. Fuente: [Microsoft Learn – Tutorial: Create and manage budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets).*

En Foundry puedes filtrar ese análisis por la etiqueta `project` para ver el gasto de cada proyecto:

![Análisis de costos de un recurso de Foundry filtrado por la etiqueta project](https://learn.microsoft.com/en-us/azure/foundry/concepts/media/manage-costs/cost-analysis-project-tag.png)

*Filtro **Tag: project** en el análisis de costos de un recurso de Foundry, con un proyecto seleccionado. Fuente: [Microsoft Learn – Manage costs in Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/concepts/manage-costs).*

---

## 7. Herramientas para trabajar con Azure

### 7.1 Azure portal
La interfaz gráfica en [portal.azure.com](https://portal.azure.com). Vale la pena conocer sus zonas:

![Portal de Azure con diez elementos numerados: menú, migas de pan, encabezado, búsqueda global, Copilot, controles globales, cuenta, barra de comandos, menú del servicio y panel de trabajo](https://learn.microsoft.com/en-us/azure/azure-portal/media/azure-portal-overview/portal-callouts.png)

*Elementos del portal. Fuente: [Microsoft Learn – Azure portal overview](https://learn.microsoft.com/en-us/azure/azure-portal/azure-portal-overview).*

| # | Elemento | Para qué sirve |
|---|---|---|
| 1 | **Menú del portal** | Navegar entre servicios. En modo *flyout* se oculta hasta que lo abres; en modo *docked* queda fijo |
| 2 | **Migas de pan** | Regresar un nivel en tu flujo |
| 3 | **Encabezado** | Barra superior con los elementos globales |
| 4 | **Búsqueda global** | Encontrar recursos, servicios o documentación (atajo `G+/`) |
| 5 | **Copilot** | Acceso a Azure Copilot |
| 6 | **Controles globales** | Cloud Shell, notificaciones, configuración, soporte y comentarios |
| 7 | **Tu cuenta** | Ver tu cuenta, cambiar de directorio (tenant) o cerrar sesión |
| 8 | **Barra de comandos** | Acciones del recurso que estás viendo (iniciar, detener, eliminar…) |
| 9 | **Menú del servicio** | Opciones del recurso: *Access control (IAM)*, *Tags*, *Locks*, *Settings*… Marca con estrella tus favoritas |
| 10 | **Panel de trabajo** | Los detalles del recurso actual (en *Essentials* verás grupo, región, suscripción y etiquetas) |

### 7.2 Azure Cloud Shell
Una terminal **Bash o PowerShell en el navegador**, ya autenticada con tu cuenta y con la CLI de Azure instalada. Ábrela desde el ícono de terminal del encabezado (elemento 6) o en [shell.azure.com](https://shell.azure.com).
- **Requisito:** la suscripción debe tener registrado el proveedor **Microsoft.CloudShell**. Basta hacerlo una vez por suscripción.
- **Sesión efímera** (*No storage account required*): arranca más rápido y no crea nada en tu suscripción, pero todo lo que guardes se borra al cerrar o reiniciar la sesión.
- **Con almacenamiento:** monta un recurso compartido de Azure Files de **5 GB** para conservar tu `$HOME` entre sesiones. Ese almacenamiento se cobra.
- **Inactividad:** la sesión se cierra tras **20 minutos** sin uso. En una sesión efímera eso borra tus archivos y tus variables.

### 7.3 Azure CLI
La herramienta `az` funciona igual en Cloud Shell, Windows, macOS y Linux:
```bash
az login                                    # abre el navegador para iniciar sesión
az account list -o table                    # tus suscripciones
az account set --subscription "<id-o-nombre-de-suscripcion>"
az account show --query "{suscripcion:name, id:id, usuario:user.name}" -o table

az group list -o table                      # -o json | jsonc | table | tsv | yaml | none
az group list --query "[?location=='eastus2'].name" -o tsv     # --query filtra con JMESPath

az configure --defaults group=rg-acordeon-ai901 location=eastus2   # valores por defecto (opcional)
az group create --help                      # ayuda y ejemplos de cualquier comando
```
- `-o tsv` devuelve texto plano, ideal para guardar un valor en una variable: `ID=$(az ... --query id -o tsv)`.
- `--query` usa **JMESPath**. `[?condición]` filtra listas y `{alias:campo}` arma tablas con las columnas que te interesan.
- Los valores de `az configure --defaults` se quedan guardados en tu CLI. Para quitarlos usa `az configure --defaults group='' location=''`.
- Si un parámetro "no existe", tu CLI probablemente es vieja. Revisa con `az version` y actualiza con `az upgrade`. Los comandos de proyectos de Foundry requieren la versión 2.80.0 o posterior.

### 7.4 Infraestructura como código (IaC)
- Con **plantillas ARM** (JSON), **Bicep** (un lenguaje más legible que se traduce a ARM) o **Terraform** describes los recursos en un archivo que puedes versionar en Git.
- Al desplegarlo, Azure deja todo **como dice el archivo**: si lo despliegas dos veces obtienes el mismo resultado, no recursos duplicados.
- Es la forma correcta de repetir un entorno (dev → prod) sin "clics" olvidados. Microsoft publica una guía para [crear un recurso de Foundry con Bicep](https://learn.microsoft.com/es-es/azure/foundry/how-to/create-resource-template).

### 7.5 Portal de Microsoft Foundry
En [ai.azure.com](https://ai.azure.com) trabajas con modelos, agentes y evaluaciones. Activa el interruptor ![Interruptor New Foundry encendido](https://learn.microsoft.com/en-us/azure/foundry/media/version-banner/new-foundry.png) para usar la experiencia nueva, que es la que describe este acordeón.

![Un recurso de Foundry con varios proyectos que comparten seguridad y gobierno; cada proyecto puede tener su propio RBAC, identidad y monitoreo](https://learn.microsoft.com/en-us/azure/foundry/media/how-to/projects/projects-multi-setup.png)

*Un **recurso** de Foundry puede tener varios **proyectos**. Cada proyecto puede tener su propio RBAC, identidad y monitoreo, pero todos heredan del recurso la seguridad de red, los despliegues de modelos y las herramientas conectadas. El primer proyecto (*default*) es el más completo: por ejemplo, Batch y fine-tuning de OpenAI solo funcionan ahí. Fuente: [Microsoft Learn – Create a project](https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects).*

| Herramienta | Cuándo usarla |
|---|---|
| [Azure Portal](https://portal.azure.com) | Explorar, crear y monitorear con interfaz gráfica |
| Azure Cloud Shell ([shell.azure.com](https://shell.azure.com)) | Usar la CLI desde el navegador, sin instalar nada |
| Azure CLI (`az`) | Automatizar con scripts |
| Plantillas Bicep / ARM o Terraform | Infraestructura como código, repetible |
| SDK de Azure para Python (`azure-identity`, `azure-mgmt-*`, `azure-keyvault-*`…) | Administrar o usar Azure desde tu propio código |
| Portal de Foundry ([ai.azure.com](https://ai.azure.com)) | Trabajar con modelos, agentes y evaluaciones |

---

## 8. Práctica en Python (sin cuenta de Azure)
Antes de tocar Azure, dos scripts que solo usan la biblioteca estándar de Python para practicar las dos fuentes de errores más comunes: **los permisos** y **los nombres**. Córrelos con `python alcances.py` y `python nombres.py`.

#### 8.1) Anatomía de un ID y herencia de permisos (`alcances.py`)
Un evaluador mínimo de RBAC con candados. Los roles son los **reales** publicados por Microsoft, recortados a las líneas que usa el ejemplo.
```python
from fnmatch import fnmatchcase

# IDs de recurso del laboratorio (la suscripción es ficticia)
SUB = "/subscriptions/00000000-0000-0000-0000-000000000000"
RG = f"{SUB}/resourceGroups/rg-acordeon-ai901"
AIF = f"{RG}/providers/Microsoft.CognitiveServices/accounts/aif-acordeon-jj"
PROJ = f"{AIF}/projects/proj-acordeon"
KV = f"{RG}/providers/Microsoft.KeyVault/vaults/kv-acordeon-jj"
SECRETO = f"{KV}/secrets/foundry-key"

# Roles integrados como los publica Microsoft (recortados a las líneas que usa este ejemplo)
ROLES = {
    "Owner": {"actions": ["*"]},
    "Contributor": {"actions": ["*"],
                    "notActions": ["Microsoft.Authorization/*/Delete", "Microsoft.Authorization/*/Write",
                                   "Microsoft.Authorization/elevateAccess/Action"]},
    "Reader": {"actions": ["*/read"]},
    "Foundry User": {"actions": ["Microsoft.Authorization/*/read", "Microsoft.CognitiveServices/*/read",
                                 "Microsoft.CognitiveServices/accounts/listkeys/action"],
                     "dataActions": ["Microsoft.CognitiveServices/*"]},
    "Key Vault Secrets Officer": {"actions": ["Microsoft.Authorization/*/read", "Microsoft.KeyVault/vaults/*/read"],
                                  "dataActions": ["Microsoft.KeyVault/vaults/secrets/*"]},
    "Key Vault Secrets User": {"dataActions": ["Microsoft.KeyVault/vaults/secrets/getSecret/action",
                                               "Microsoft.KeyVault/vaults/secrets/readMetadata/action"]},
}

# Asignación de rol = QUIÉN + QUÉ ROL + EN QUÉ ÁMBITO
ASIGNACIONES = [
    ("jesus", "Owner", SUB),                          # creó la suscripción
    ("luis", "Contributor", RG),                      # administra la infraestructura del laboratorio
    ("ana", "Reader", AIF),                           # desarrolladora: ve el recurso de Foundry...
    ("ana", "Foundry User", PROJ),                    # ...y construye solo en SU proyecto
    ("id-acordeon-app", "Key Vault Secrets User", KV),
    ("id-acordeon-app", "Foundry User", AIF),
]
CANDADOS = [("no-borrar-lab", "CanNotDelete", RG)]


def anatomia(rid):
    """Divide un ID de recurso en sus niveles y calcula el tipo (proveedor/tipo[/subtipo])."""
    p = rid.strip("/").split("/")
    niveles = ["/" + "/".join(p[0:2]), "/" + "/".join(p[2:4]), "/" + "/".join(p[4:8])]
    niveles += ["/" + "/".join(p[i:i + 2]) for i in range(8, len(p), 2)]
    resto = p[6:]                                      # después de providers/<espacio de nombres>
    tipo = "/".join([p[5]] + resto[0::2])
    return niveles, tipo


def aplica(ambito, recurso):
    """Una asignación (o un candado) aplica al recurso si su ámbito es el recurso o uno de sus 'ancestros'."""
    a, r = ambito.lower(), recurso.lower()
    return r == a or r.startswith(a + "/")


def coincide(patrones, operacion):
    return any(fnmatchcase(operacion.lower(), p.lower()) for p in patrones)


def rol_permite(rol, operacion, es_dato):
    d = ROLES[rol]
    si, no = ("dataActions", "notDataActions") if es_dato else ("actions", "notActions")
    return coincide(d.get(si, []), operacion) and not coincide(d.get(no, []), operacion)


def evaluar(quien, operacion, recurso, es_dato):
    roles = [rol for p, rol, ambito in ASIGNACIONES if p == quien and aplica(ambito, recurso)]
    otorgan = [rol for rol in roles if rol_permite(rol, operacion, es_dato)]
    if not otorgan:
        return "NO", f"ningún rol lo permite (aplican: {', '.join(roles) or 'ninguno'})"
    if not es_dato:                                    # los candados solo afectan al plano de control
        op = operacion.lower()
        for _, nivel, ambito in CANDADOS:
            bloquea = op.endswith("/delete") if nivel == "CanNotDelete" else not op.endswith("/read")
            if aplica(ambito, recurso) and bloquea:
                return "NO", f"candado {nivel} ({otorgan[0]} lo permitiría)"
    return "SÍ", f"lo permite {' + '.join(otorgan)}"


niveles, tipo = anatomia(PROJ)
print("Niveles del ID del proyecto:")
for i, nivel in enumerate(niveles):
    print("  " + "   " * i + ("└─ " if i else "") + nivel)
print(f"Tipo de recurso: {tipo}\n")

print("Asignaciones que llegan (por herencia) hasta el proyecto:")
for quien, rol, ambito in ASIGNACIONES:
    if aplica(ambito, PROJ):
        print(f"  {quien:<15} {rol:<13} asignado en {'/'.join(ambito.split('/')[-2:])}")

AGENTES = "Microsoft.CognitiveServices/accounts/AIServices/agents/write"
PREGUNTAS = [
    ("jesus", "borrar el grupo de recursos", "Microsoft.Resources/subscriptions/resourceGroups/delete", RG, False),
    ("jesus", "leer el secreto foundry-key", "Microsoft.KeyVault/vaults/secrets/getSecret/action", SECRETO, True),
    ("jesus", "asignar un rol en la bóveda", "Microsoft.Authorization/roleAssignments/write", KV, False),
    ("luis", "crear otro proyecto", "Microsoft.CognitiveServices/accounts/projects/write",
     f"{AIF}/projects/proj-nuevo", False),
    ("luis", "crear un agente", AGENTES, PROJ, True),
    ("luis", "dar acceso a Ana", "Microsoft.Authorization/roleAssignments/write", PROJ, False),
    ("luis", "crear un candado", "Microsoft.Authorization/locks/write", RG, False),
    ("luis", "borrar la bóveda", "Microsoft.KeyVault/vaults/delete", KV, False),
    ("ana", "ver el recurso de Foundry", "Microsoft.CognitiveServices/accounts/read", AIF, False),
    ("ana", "crear agente en SU proyecto", AGENTES, PROJ, True),
    ("ana", "crear agente en otro proyecto", AGENTES, f"{AIF}/projects/proj-otro", True),
    ("ana", "desplegar un modelo", "Microsoft.CognitiveServices/accounts/deployments/write", AIF, False),
    ("id-acordeon-app", "leer el secreto foundry-key", "Microsoft.KeyVault/vaults/secrets/getSecret/action",
     SECRETO, True),
    ("id-acordeon-app", "cambiar el secreto", "Microsoft.KeyVault/vaults/secrets/setSecret/action",
     SECRETO, True),
]

print("\n¿Quién puede hacer qué?")
for quien, que, operacion, recurso, es_dato in PREGUNTAS:
    veredicto, motivo = evaluar(quien, operacion, recurso, es_dato)
    plano = "datos" if es_dato else "control"
    print(f"  {quien:<15} {que:<29} [{plano:<7}] {veredicto:<2}  {motivo}")

ASIGNACIONES.append(("jesus", "Key Vault Secrets Officer", KV))     # lo que harás en el Paso 9 del tutorial
veredicto, _ = evaluar("jesus", "Microsoft.KeyVault/vaults/secrets/getSecret/action", SECRETO, True)
print(f"\nPaso 9 del tutorial (jesus + Key Vault Secrets Officer en la bóveda) -> leer el secreto: {veredicto}")
```

Salida:
```
Niveles del ID del proyecto:
  /subscriptions/00000000-0000-0000-0000-000000000000
     └─ /resourceGroups/rg-acordeon-ai901
        └─ /providers/Microsoft.CognitiveServices/accounts/aif-acordeon-jj
           └─ /projects/proj-acordeon
Tipo de recurso: Microsoft.CognitiveServices/accounts/projects

Asignaciones que llegan (por herencia) hasta el proyecto:
  jesus           Owner         asignado en subscriptions/00000000-0000-0000-0000-000000000000
  luis            Contributor   asignado en resourceGroups/rg-acordeon-ai901
  ana             Reader        asignado en accounts/aif-acordeon-jj
  ana             Foundry User  asignado en projects/proj-acordeon
  id-acordeon-app Foundry User  asignado en accounts/aif-acordeon-jj

¿Quién puede hacer qué?
  jesus           borrar el grupo de recursos   [control] NO  candado CanNotDelete (Owner lo permitiría)
  jesus           leer el secreto foundry-key   [datos  ] NO  ningún rol lo permite (aplican: Owner)
  jesus           asignar un rol en la bóveda   [control] SÍ  lo permite Owner
  luis            crear otro proyecto           [control] SÍ  lo permite Contributor
  luis            crear un agente               [datos  ] NO  ningún rol lo permite (aplican: Contributor)
  luis            dar acceso a Ana              [control] NO  ningún rol lo permite (aplican: Contributor)
  luis            crear un candado              [control] NO  ningún rol lo permite (aplican: Contributor)
  luis            borrar la bóveda              [control] NO  candado CanNotDelete (Contributor lo permitiría)
  ana             ver el recurso de Foundry     [control] SÍ  lo permite Reader
  ana             crear agente en SU proyecto   [datos  ] SÍ  lo permite Foundry User
  ana             crear agente en otro proyecto [datos  ] NO  ningún rol lo permite (aplican: Reader)
  ana             desplegar un modelo           [control] NO  ningún rol lo permite (aplican: Reader)
  id-acordeon-app leer el secreto foundry-key   [datos  ] SÍ  lo permite Key Vault Secrets User
  id-acordeon-app cambiar el secreto            [datos  ] NO  ningún rol lo permite (aplican: Key Vault Secrets User)

Paso 9 del tutorial (jesus + Key Vault Secrets Officer en la bóveda) -> leer el secreto: SÍ
```
- **Explicación:**
  - `anatomia()` parte el ID en niveles. El tipo `Microsoft.CognitiveServices/accounts/projects` sale de juntar el proveedor con los tipos de cada nivel.
  - `aplica()` es la **herencia**: una asignación sirve si su ámbito es un prefijo del ID, completo por segmentos. Por eso el *Owner* de la suscripción alcanza al proyecto, pero el *Foundry User* de `ana` en su proyecto **no** sube al recurso padre ni pasa a `proj-otro`.
  - `rol_permite()` revisa `actions` o `dataActions` según el plano. `NotActions` **no es una denegación**: solo recorta lo que da *ese* rol. Si otro rol tuyo lo permite, se permite, porque el modelo es **aditivo**.
  - Los **candados** solo se revisan en el plano de control y aplican a todos, Owner incluido. *CanNotDelete* frena los `/delete`; *ReadOnly* frena todo lo que no sea `/read`.
  - **Cómo leer la salida:**
    - `jesus` es Owner y aun así no puede borrar el grupo, por el candado, ni leer el secreto, porque Owner no tiene `dataActions`. Lo segundo cambia en el [Paso 9](#paso-9-guarda-la-llave-en-key-vault).
    - `luis`, como Contributor, crea proyectos, pero no puede construir agentes, asignar roles ni crear candados.
    - `ana` solo construye en *su* proyecto y no puede desplegar modelos.
    - La identidad de la app lee el secreto, pero no puede cambiarlo: eso es **mínimo privilegio**.
  - **Simplificaciones:** no modela asignaciones de denegación, condiciones (ABAC), grupos anidados ni la lista completa de acciones de cada rol.
  - **Pruébalo:** cambia `"CanNotDelete"` por `"ReadOnly"` en `CANDADOS` y vuelve a correrlo. Ahora `luis` ya ni siquiera puede crear otro proyecto, ni `jesus` asignar roles. En cambio, `ana` sigue construyendo agentes y la app sigue leyendo el secreto, porque el candado no toca el plano de datos.

#### 8.2) Valida tus nombres antes de crear nada (`nombres.py`)
Las reglas de la tabla de la [sección 5.4](#54-convención-de-nombres), convertidas en código. Cambia `INI` por tus iniciales.
```python
import re

# Reglas oficiales de nombres (Microsoft Learn) + abreviatura recomendada por el Cloud Adoption Framework
REGLAS = {
    "Grupo de recursos": {"caf": "rg", "min": 1, "max": 90, "unico": "la suscripción",
                          "ok": r"[\w.()-]+", "txt": "letras, dígitos, _ . ( ) -", "no_fin": "."},
    "Recurso de Foundry": {"caf": "aif", "min": 2, "max": 64, "unico": "todo Azure (por el subdominio)",
                           "ok": r"[A-Za-z0-9-]+", "txt": "alfanuméricos y guiones", "extremos": "alnum"},
    "Key Vault": {"caf": "kv", "min": 3, "max": 24, "unico": "todo Azure",
                  "ok": r"[A-Za-z0-9-]+", "txt": "alfanuméricos y guiones", "inicio_letra": True,
                  "extremos": "fin", "sin_dobles": True},
    "Identidad administrada": {"caf": "id", "min": 3, "max": 128, "unico": "el grupo de recursos",
                               "ok": r"[A-Za-z0-9_-]+", "txt": "alfanuméricos, _ y -", "extremos": "inicio"},
    "Cuenta de almacenamiento": {"caf": "st", "min": 3, "max": 24, "unico": "todo Azure",
                                 "ok": r"[a-z0-9]+", "txt": "solo minúsculas y números"},
    "Secreto de Key Vault": {"min": 1, "max": 127, "unico": "la bóveda",
                             "ok": r"[A-Za-z0-9-]+", "txt": "alfanuméricos y guiones"},
}


def validar(tipo, nombre):
    r, errores = REGLAS[tipo], []
    if not r["min"] <= len(nombre) <= r["max"]:
        errores.append(f"mide {len(nombre)} (permitido: {r['min']}-{r['max']})")
    if not re.fullmatch(r["ok"], nombre):
        errores.append(f"tiene caracteres no permitidos ({r['txt']})")
    if r.get("no_fin") and nombre.endswith(r["no_fin"]):
        errores.append(f"no puede terminar en '{r['no_fin']}'")
    if r.get("inicio_letra") and not nombre[:1].isalpha():
        errores.append("debe empezar con letra")
    extremos = r.get("extremos")
    if extremos in ("alnum", "inicio") and not nombre[:1].isalnum():
        errores.append("debe empezar con letra o número")
    if extremos in ("alnum", "fin") and not nombre[-1:].isalnum():
        errores.append("debe terminar con letra o número")
    if r.get("sin_dobles") and "--" in nombre:
        errores.append("no admite guiones seguidos")
    avisos = []
    if r.get("caf") and not errores and not nombre.startswith(r["caf"]):
        avisos.append(f"válido, pero el CAF sugiere el prefijo '{r['caf']}'")
    return errores, avisos


def reporte(titulo, candidatos):
    print(titulo)
    for tipo, nombre in candidatos:
        errores, avisos = validar(tipo, nombre)
        marca = "✘" if errores else ("!" if avisos else "✔")
        detalle = "; ".join(errores or avisos) or f"debe ser único en {REGLAS[tipo]['unico']}"
        print(f"  {marca} {tipo:<24} {nombre:<28} {detalle}")


INI = "jj"                                   # tus iniciales: cámbialas
PLAN = [("Grupo de recursos", "rg-acordeon-ai901"), ("Recurso de Foundry", f"aif-acordeon-{INI}"),
        ("Key Vault", f"kv-acordeon-{INI}"), ("Identidad administrada", "id-acordeon-app"),
        ("Secreto de Key Vault", "foundry-key")]
TROPIEZOS = [("Key Vault", "kv-acordeon-ai901-jesus-dev"), ("Key Vault", "kv--acordeon"),
             ("Key Vault", "1kv-acordeon"), ("Key Vault", "boveda-acordeon"),
             ("Cuenta de almacenamiento", "st-acordeon-jj"), ("Recurso de Foundry", "aif-acordeon-jj-"),
             ("Secreto de Key Vault", "foundry_key"), ("Grupo de recursos", "rg-acordeon.")]

reporte("Nombres del laboratorio:", PLAN)
reporte("\nTropiezos comunes:", TROPIEZOS)

if all(not validar(t, n)[0] for t, n in PLAN):
    print("\nTodo en orden. Variables para el tutorial:")
    for var, (_, nombre) in zip(["RG", "AIF", "KV", "ID"], PLAN):
        print(f"{var}={nombre}")
```

Salida:
```
Nombres del laboratorio:
  ✔ Grupo de recursos        rg-acordeon-ai901            debe ser único en la suscripción
  ✔ Recurso de Foundry       aif-acordeon-jj              debe ser único en todo Azure (por el subdominio)
  ✔ Key Vault                kv-acordeon-jj               debe ser único en todo Azure
  ✔ Identidad administrada   id-acordeon-app              debe ser único en el grupo de recursos
  ✔ Secreto de Key Vault     foundry-key                  debe ser único en la bóveda

Tropiezos comunes:
  ✘ Key Vault                kv-acordeon-ai901-jesus-dev  mide 27 (permitido: 3-24)
  ✘ Key Vault                kv--acordeon                 no admite guiones seguidos
  ✘ Key Vault                1kv-acordeon                 debe empezar con letra
  ! Key Vault                boveda-acordeon              válido, pero el CAF sugiere el prefijo 'kv'
  ✘ Cuenta de almacenamiento st-acordeon-jj               tiene caracteres no permitidos (solo minúsculas y números)
  ✘ Recurso de Foundry       aif-acordeon-jj-             debe terminar con letra o número
  ✘ Secreto de Key Vault     foundry_key                  tiene caracteres no permitidos (alfanuméricos y guiones)
  ✘ Grupo de recursos        rg-acordeon.                 no puede terminar en '.'

Todo en orden. Variables para el tutorial:
RG=rg-acordeon-ai901
AIF=aif-acordeon-jj
KV=kv-acordeon-jj
ID=id-acordeon-app
```
- **Explicación:**
  - Cada regla viene de la tabla oficial de nombres de Azure. La abreviatura (`rg`, `aif`, `kv`, `id`, `st`) es la recomendación del Cloud Adoption Framework y por eso solo genera un **aviso** (`!`), no un error.
  - **Tropiezos comunes:**
    - Bóvedas de más de 24 caracteres.
    - Guiones en cuentas de almacenamiento.
    - Guiones bajos en nombres de secretos.
    - Nombres que terminan en guion o en punto.
  - Lo que **no** puede revisar un script sin conexión es la **unicidad global**. Si `aif-acordeon-jj` ya existe en algún lugar de Azure, la creación fallará con `CustomDomainInUse` y tendrás que cambiar `INI`.
  - Las últimas líneas son las variables que usarás en el [Paso 3](#paso-3-define-tus-variables) del tutorial.

---

## 9. Tutorial: tu primer laboratorio en Azure, paso a paso
Vas a construir, revisar y desmontar un laboratorio completo:
- Un **grupo de recursos** etiquetado, `rg-acordeon-ai901`, y un **presupuesto** con alertas.
- Un **recurso de Foundry**, `aif-acordeon-<tus-iniciales>`, con su **proyecto** `proj-acordeon` y los **roles mínimos** para ti y para el proyecto.
- Una **bóveda** con RBAC, `kv-acordeon-<tus-iniciales>`, que guarda la llave de Foundry como secreto.
- Una **identidad administrada**, `id-acordeon-app`, lista para tu futura aplicación.
- Una **revisión desde Python** sin llaves en el código, un **candado** contra borrados accidentales y, al final, **limpieza total**.

**Antes de empezar:**
- **Necesitas** una suscripción en la que seas **Owner**. Normalmente lo eres si tú creaste la cuenta.
- **Tiempo:** de 45 a 60 minutos.
- **Costo:** el laboratorio no despliega modelos ni hace inferencia, así que el consumo debería ser mínimo (por ejemplo, unas cuantas operaciones de Key Vault). Aun así, crea el presupuesto ([Paso 6](#paso-6-crea-un-presupuesto-con-alertas)) y no te saltes la limpieza ([Paso 15](#paso-15-limpieza-total)).

> [!TIP]
> En una sesión efímera de Cloud Shell, si se cierra la pestaña o pasan 20 minutos sin actividad, **pierdes tus variables**. Vuelve a correr el bloque del [Paso 3](#paso-3-define-tus-variables) antes de continuar.

#### Paso 0. Consigue una suscripción
- Elige una opción de la tabla de la [sección 3.6](#36-suscripciones-y-tipos-de-cuenta):
  - [Cuenta gratuita](https://azure.microsoft.com/pricing/purchase-options/azure-account).
  - [Azure for Students](https://azure.microsoft.com/free/students/), sin tarjeta.
  - La suscripción de tu empresa o escuela.
- **Si la suscripción es de tu organización,** pregunta qué rol tienes:
  - Sin **Owner** (o *User Access Administrator*) no podrás asignar roles en los Pasos 8 a 10, ni crear el candado del Paso 13.
  - Para **purgar** en el Paso 15 hacen falta permisos a nivel de suscripción.

#### Paso 1. Recorre el portal
Los nombres de menús están en inglés, como en las capturas. Si tu portal está en español, las opciones equivalentes aparecen traducidas.
1. Entra a [portal.azure.com](https://portal.azure.com) y ubica los elementos de la [sección 7.1](#71-azure-portal): menú, búsqueda global, Cloud Shell y tu cuenta.
2. En la búsqueda global escribe **Subscriptions**, abre tu suscripción y anota su **Subscription ID**.
3. En el menú de la suscripción abre **Settings › My permissions** para ver tu rol, y **Access control (IAM) › Role assignments** para ver quién tiene qué.
4. Abre **Settings › Resource providers**. Lo usarás en el siguiente paso.

#### Paso 2. Abre Cloud Shell
1. **Registra el proveedor de Cloud Shell** si nunca lo has usado en esta suscripción: **Settings › Resource providers** → busca `cloudshell` → selecciona **Microsoft.CloudShell** → **Register**.

   ![Página Resource providers de una suscripción con Microsoft.CloudShell seleccionado y el botón Register resaltado](https://learn.microsoft.com/en-us/azure/cloud-shell/get-started/media/ephemeral/resource-provider.png)

   *Registro de **Microsoft.CloudShell**: estado *unregistered* → **Register**. Basta una vez por suscripción. Fuente: [Microsoft Learn – Get started with Azure Cloud Shell ephemeral sessions](https://learn.microsoft.com/en-us/azure/cloud-shell/get-started/ephemeral).*
2. Abre **Cloud Shell** desde el ícono de terminal del encabezado y elige **Bash**.

   ![Ventana de bienvenida de Azure Cloud Shell con los botones Bash y PowerShell](https://learn.microsoft.com/en-us/azure/cloud-shell/get-started/media/ephemeral/choose-shell.png)

   *La primera vez eliges entre Bash y PowerShell. Después puedes cambiar desde la barra de Cloud Shell. Fuente: [Microsoft Learn – Get started with Azure Cloud Shell ephemeral sessions](https://learn.microsoft.com/en-us/azure/cloud-shell/get-started/ephemeral).*
3. En **Getting started** selecciona **No storage account required**, elige tu suscripción y pulsa **Apply**.

   ![Panel Getting started de Cloud Shell con la opción No storage account required seleccionada](https://learn.microsoft.com/en-us/azure/cloud-shell/get-started/media/ephemeral/getting-started.png)

   *Sesión efímera: no crea nada en tu suscripción, pero sus archivos desaparecen al terminar. Fuente: [Microsoft Learn – Get started with Azure Cloud Shell ephemeral sessions](https://learn.microsoft.com/en-us/azure/cloud-shell/get-started/ephemeral).*
4. Comprueba quién eres y qué versión de la CLI tienes:
   ```bash
   az account show --query "{suscripcion:name, id:id, usuario:user.name}" -o table
   az version --query '"azure-cli"' -o tsv
   ```

¿Prefieres tu PC? Instala la CLI, corre `az login` y `az account set --subscription "<id>"`. Todos los comandos del tutorial son iguales.

#### Paso 3. Define tus variables
Si corriste [`nombres.py`](#82-valida-tus-nombres-antes-de-crear-nada-nombrespy), ya sabes que estos nombres cumplen las reglas.
```bash
# ── Ajusta estas tres ──
INI=jj                      # tus iniciales en minúsculas (vuelven únicos los nombres globales)
LOC=eastus2                 # región del laboratorio
RG=rg-acordeon-ai901

# ── Derivadas ──
AIF=aif-acordeon-$INI       # recurso de Foundry; también será su subdominio (único en todo Azure)
PROJ=proj-acordeon
KV=kv-acordeon-$INI         # bóveda: 3 a 24 caracteres, única en todo Azure
ID=id-acordeon-app          # identidad administrada para tu futura app
FOUNDRY_USER=53ca6127-db72-4b80-b1b0-d745d6d5456d    # ID del rol Foundry User (antes "Azure AI User")

SUB_ID=$(az account show --query id -o tsv)
YO=$(az ad signed-in-user show --query id -o tsv)    # tu objectId en Microsoft Entra ID
echo "Suscripción: $SUB_ID | Tu objectId: $YO"
```
- `SUB_ID` y `YO` se calculan con la CLI. Las demás variables son nombres que tú eliges.
- Para el rol de Foundry usamos el **ID del rol** y no el nombre, como recomienda Microsoft mientras termina el cambio de nombre de los roles.

#### Paso 4. Revisa los proveedores de recursos
```bash
for ns in Microsoft.CognitiveServices Microsoft.KeyVault Microsoft.ManagedIdentity; do
  echo "$ns -> $(az provider show --namespace $ns --query registrationState -o tsv)"
done

# Solo si alguno aparece como NotRegistered (cambia el nombre del proveedor):
az provider register --namespace Microsoft.CognitiveServices --wait
```
- Registra **solo** los proveedores que vas a usar (mínimo privilegio).
- Si te saltas este paso y un proveedor no está registrado, la creación fallará con `MissingSubscriptionRegistration`.

#### Paso 5. Crea el grupo de recursos con etiquetas
```bash
az group create --name $RG --location $LOC \
  --tags proyecto=acordeon-ai901 entorno=lab responsable=$INI

az group show --name $RG --query "{nombre:name, region:location, etiquetas:tags}" -o json
```
- La región del grupo define **dónde se guardan sus metadatos**.
- Las etiquetas te servirán para filtrar costos. Recuerda que **no** pasan a los recursos que crees dentro.

#### Paso 6. Crea un presupuesto con alertas
En el portal (las pantallas son las de la [sección 6.2](#62-presupuestos-y-alertas)):
1. Busca **Cost Management** y entra a **Budgets**.
2. Revisa que el **Scope** sea tu suscripción, o cámbialo al grupo `rg-acordeon-ai901`. Luego pulsa **Add**.
3. Llena el formulario y pulsa **Next**:
   - Nombre: `budget-acordeon-ai901`.
   - *Reset period*: **Monthly**.
   - *Amount*: un monto bajo, por ejemplo 10 en la moneda de tu cuenta.
4. Agrega tres alertas y tu correo, y pulsa **Create**:
   - **Actual** al 50 %.
   - **Actual** al 90 %.
   - **Forecasted** al 100 %.

Recuerda que el presupuesto **avisa, no detiene**, y que se evalúa cada 24 horas con datos de 8 a 24 horas de antigüedad.

#### Paso 7. Crea el recurso de Foundry y su proyecto
**Con la CLI**, siguiendo la guía oficial de Microsoft (le agregamos etiquetas; requiere CLI 2.80.0 o posterior):
```bash
az cognitiveservices account create \
  --name $AIF \
  --resource-group $RG \
  --kind AIServices \
  --sku S0 \
  --location $LOC \
  --custom-domain $AIF \
  --assign-identity \
  --allow-project-management true \
  --tags proyecto=acordeon-ai901 entorno=lab

az cognitiveservices account project create \
  --name $AIF \
  --resource-group $RG \
  --project-name $PROJ \
  --location $LOC

# Las dos deben responder: Succeeded
az cognitiveservices account show -n $AIF -g $RG --query properties.provisioningState -o tsv
az cognitiveservices account project show -n $AIF -g $RG --project-name $PROJ \
  --query properties.provisioningState -o tsv

az cognitiveservices account show -n $AIF -g $RG --query properties.endpoints -o json
echo "Endpoint del proyecto: https://$AIF.services.ai.azure.com/api/projects/$PROJ"
```
- **Explicación:**
  - El recurso de Foundry es de tipo `AIServices` (proveedor `Microsoft.CognitiveServices`).
  - `--custom-domain` crea el subdominio `https://<nombre>.services.ai.azure.com`, que es **obligatorio** para autenticarte con Entra ID y debe ser **único en todo Azure**. Si ya existe, verás `CustomDomainInUse`: cambia `INI` y repite.
  - `--assign-identity` crea la **identidad administrada** del recurso. Sin ella, crear el proyecto falla con un error que pide habilitar una identidad administrada.
  - `--allow-project-management true` habilita los **proyectos** y **no se puede cambiar después** de crear el recurso.
  - El proyecto se crea con su propia identidad administrada asignada por el sistema. La usarás en el siguiente paso.
  - El último comando imprime el **endpoint del proyecto** que usan el SDK de Foundry y los temas siguientes.

**Alternativa en el portal de Foundry:**
1. Entra a [ai.azure.com](https://ai.azure.com) con el interruptor **New Foundry** encendido.
2. Selecciona el nombre del proyecto en la esquina superior izquierda y elige **Create new project**.
3. Ponle nombre y pulsa **Create project**. En las opciones avanzadas eliges el grupo de recursos y la región.

Ese camino crea el recurso con valores por defecto y, si puedes asignar roles, también hace las asignaciones del Paso 8 por ti.

#### Paso 8. Asigna los roles de Foundry
Desde la CLI **nadie** recibe el rol *Foundry User* automáticamente. Sin él, tú no podrías construir agentes aunque seas Owner, y la identidad del proyecto no tendría acceso a las funciones de Foundry:
```bash
AIF_ID=$(az cognitiveservices account show -n $AIF -g $RG --query id -o tsv)
PROJ_MI=$(az cognitiveservices account project show -n $AIF -g $RG --project-name $PROJ \
  --query identity.principalId -o tsv)

# Tú: Foundry User sobre el recurso
az role assignment create --role $FOUNDRY_USER \
  --assignee-object-id $YO --assignee-principal-type User --scope $AIF_ID

# La identidad administrada del proyecto: también Foundry User sobre el recurso
az role assignment create --role $FOUNDRY_USER \
  --assignee-object-id $PROJ_MI --assignee-principal-type ServicePrincipal --scope $AIF_ID

az role assignment list --scope $AIF_ID \
  --query "[].{rol:roleDefinitionName, quien:principalName, tipo:principalType}" -o table
```
- `--assignee-object-id` junto con `--assignee-principal-type` evita errores cuando la identidad es muy reciente y Entra ID aún no la "ve" en todas partes.
- **Para un compañero de equipo,** asigna el rol en el ámbito del **proyecto**. Así solo construye ahí (mínimo privilegio):
  ```bash
  PROJECT_ID=$(az cognitiveservices account project show -n $AIF -g $RG --project-name $PROJ --query id -o tsv)
  az role assignment create --role $FOUNDRY_USER \
    --assignee "companera@contoso.com" --scope $PROJECT_ID
  ```

#### Paso 9. Guarda la llave en Key Vault
```bash
az keyvault create --name $KV --resource-group $RG --location $LOC \
  --enable-rbac-authorization true --retention-days 7 \
  --tags proyecto=acordeon-ai901 entorno=lab
KV_ID=$(az keyvault show --name $KV --query id -o tsv)

# Ser Owner NO te deja leer ni escribir secretos: necesitas un rol de DATOS
az role assignment create --role "Key Vault Secrets Officer" \
  --assignee-object-id $YO --assignee-principal-type User --scope $KV_ID
# … espera uno o dos minutos a que el permiso se propague …

# Guarda la llave de Foundry sin que aparezca en pantalla
az keyvault secret set --vault-name $KV --name foundry-key \
  --value "$(az cognitiveservices account keys list -n $AIF -g $RG --query key1 -o tsv)" \
  --output none

az keyvault secret show --vault-name $KV --name foundry-key \
  --query "{nombre:name, habilitado:attributes.enabled, creado:attributes.created}" -o table
```
- **Explicación:**
  - `--enable-rbac-authorization true` usa el modelo **RBAC**, el predeterminado en las bóvedas nuevas.
  - `--retention-days 7` deja la **retención mínima** de la eliminación temporal, para que el nombre se libere pronto cuando borres el laboratorio. La **protección de purga** se queda apagada a propósito: es irreversible. En producción, actívala.
  - El rol *Key Vault Secrets Officer* es lo que convierte el "NO" de [`alcances.py`](#81-anatomía-de-un-id-y-herencia-de-permisos-alcancespy) en "SÍ".
  - `$(…)` mete la llave directamente en el secreto y `--output none` evita que la CLI la imprima.
  - Lo ideal es que tus apps **no necesiten la llave** y usen Entra ID. La bóveda es para las herramientas que todavía solo aceptan llaves.

Si intentas crear un secreto sin el rol de datos, el portal te responde así:

![Formulario Create a secret con el error The operation is not allowed by RBAC](https://learn.microsoft.com/en-us/azure/key-vault/media/rbac/image-11.png)

*"The operation is not allowed by RBAC": te falta un rol de datos en la bóveda, o todavía no se propaga. Fuente: [Microsoft Learn – Azure RBAC para Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide).*

> [!WARNING]
> Nunca compartas tus llaves ni las subas a GitHub. Si se filtran, **regenéralas** desde el portal (*Keys and Endpoint → Regenerate*) y actualiza el secreto.

#### Paso 10. Crea una identidad administrada para tu futura app
```bash
az identity create --name $ID --resource-group $RG --location $LOC
MI=$(az identity show --name $ID --resource-group $RG --query principalId -o tsv)

az role assignment create --role "Key Vault Secrets User" \
  --assignee-object-id $MI --assignee-principal-type ServicePrincipal --scope $KV_ID
az role assignment create --role $FOUNDRY_USER \
  --assignee-object-id $MI --assignee-principal-type ServicePrincipal --scope $AIF_ID
```
- Es una identidad **asignada por el usuario**: vive aparte y la podrás conectar a la App Service, Container App o VM que ejecute tu código.
- Con *Foundry User* tu app puede llamar a Foundry **con tokens, sin llave**. Con *Key Vault Secrets User* puede **leer**, pero no cambiar, los secretos. Es la misma combinación que `id-acordeon-app` tiene en `alcances.py`.
- La creamos **sin etiquetas** a propósito: la usarás en el Paso 12.

#### Paso 11. Revisa tu laboratorio desde Python (`revisar_lab.py`)
Puedes correrlo en Cloud Shell o en tu PC después de `az login`. Crea el archivo con el editor que prefieras, por ejemplo `nano revisar_lab.py`.
```bash
python3 -m venv .venv && source .venv/bin/activate     # Windows: python -m venv .venv; .venv\Scripts\Activate.ps1
pip install azure-identity azure-mgmt-resource azure-keyvault-secrets
export AZURE_SUBSCRIPTION_ID=$SUB_ID RG KV
```

```python
import os

from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.mgmt.resource.resources import ResourceManagementClient

suscripcion = os.environ["AZURE_SUBSCRIPTION_ID"]
grupo = os.environ.get("RG", "rg-acordeon-ai901")
boveda = os.environ["KV"]

# Local: usa tu sesión de `az login`. Dentro de Azure: la identidad administrada del servicio.
credencial = DefaultAzureCredential()

# 1) Plano de CONTROL (management.azure.com): ¿qué hay en el grupo de recursos?
arm = ResourceManagementClient(credencial, suscripcion)
print(f"Recursos en {grupo}:")
for r in arm.resources.list_by_resource_group(grupo):
    etiquetas = ", ".join(f"{k}={v}" for k, v in (r.tags or {}).items()) or "(sin etiquetas)"
    print(f"  {r.type:<50} {r.name:<18} {r.location:<8} {etiquetas}")

# 2) Plano de DATOS (<bóveda>.vault.azure.net): leer el secreto SIN imprimirlo
secretos = SecretClient(vault_url=f"https://{boveda}.vault.azure.net", credential=credencial)
try:
    secreto = secretos.get_secret("foundry-key")
except HttpResponseError as e:
    if e.status_code == 403:
        raise SystemExit("403 de Key Vault: tu identidad no tiene un rol de DATOS en la bóveda "
                         "(Key Vault Secrets User u Officer). Ser Owner no basta.")
    raise
print(f"\nSecreto '{secreto.name}' leído: {len(secreto.value)} caracteres, "
      f"versión creada el {secreto.properties.created_on:%Y-%m-%d}.")
```
- **Explicación:**
  - **Una sola credencial, dos planos:**
    - `DefaultAzureCredential` pide un token para `management.azure.com` (ARM, plano de control) y otro para `vault.azure.net` (Key Vault, plano de datos).
    - En tu PC usa tu sesión de `az login`. Dentro de Azure usaría la identidad administrada del Paso 10, **sin cambiar el código**.
  - **Recursos del grupo:** `list_by_resource_group` devuelve cada recurso con su **tipo**, nombre, región y etiquetas. Comprueba que `id-acordeon-app` sale **sin etiquetas**.
  - **El secreto:** se lee, pero solo se imprime su **longitud**. Nunca imprimas secretos en logs.
  - **Si Key Vault responde 403,** el script lo traduce: te falta un rol de **datos**. Ser Owner no basta.
  - **Instalación:** con `azure-mgmt-resource` 26 o posterior, el cliente se importa desde `azure.mgmt.resource.resources`.

**Pruébalo.** Quítate el rol de datos y vuelve a correr el script:
```bash
az role assignment delete --role "Key Vault Secrets Officer" --assignee $YO --scope $KV_ID
# … espera unos minutos: quitar un rol también tarda en propagarse …
python revisar_lab.py          # ahora termina con el mensaje del 403

az role assignment create --role "Key Vault Secrets Officer" \
  --assignee-object-id $YO --assignee-principal-type User --scope $KV_ID
```
En el portal, la pestaña **Secrets** de tu bóveda se verá así mientras no tengas el rol:

![Pestaña Secrets de una bóveda con el aviso The operation is not allowed by RBAC y el mensaje You are unauthorized to view these contents](https://learn.microsoft.com/en-us/azure/key-vault/media/rbac/image-13.png)

*Sin un rol de datos, el portal muestra la bóveda pero no su contenido. Fuente: [Microsoft Learn – Azure RBAC para Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide).*

#### Paso 12. Etiquetas: agrega, consulta y comprueba que no se heredan
```bash
az tag update --resource-id $KV_ID --operation Merge --tags dato=sensible

az resource list --resource-group $RG --query "[].{nombre:name, tipo:type, etiquetas:tags}" -o json
az resource list --tag proyecto=acordeon-ai901 --query "[].name" -o tsv
```
- `--operation Merge` **agrega** la etiqueta sin borrar las que ya tenía. `Replace` sustituye todas y `Delete` quita las indicadas.
- La identidad `id-acordeon-app` **no** aparece en la búsqueda por `proyecto`: el grupo tiene esa etiqueta, pero no se hereda. Para heredarlas automáticamente usarías una Azure Policy.

#### Paso 13. Protege el laboratorio con un candado
```bash
az lock create --name no-borrar-lab --lock-type CanNotDelete \
  --resource-group $RG --notes "Laboratorio AI-901: quitar antes de limpiar"
az lock list --resource-group $RG -o table

# Prueba: intenta borrar la identidad (es barata de recrear). Debe FALLAR con ScopeLocked
az identity delete --name $ID --resource-group $RG
```
- El candado se **hereda** a todo el grupo y frena a **cualquiera**, Owner incluido.
- Si el borrado *funcionó*, el candado no se aplicó: revisa `az lock list` y recrea la identidad (Paso 10).
- Un candado también protege los **recursos de extensión** de su ámbito, como las asignaciones de rol. Por eso el ejercicio del 403 va antes de este paso.
- En el portal: grupo de recursos → **Settings › Locks** → **Add**, como en la [sección 5.2](#52-candados-resource-locks).

#### Paso 14. Revisa los costos
1. En el portal, abre **Cost Management › Cost analysis** y cambia el **Scope** a `rg-acordeon-ai901`.
2. Agrupa por **Resource** o filtra por la etiqueta `proyecto`, como en la [sección 6.3](#63-análisis-de-costos).
3. Vuelve al día siguiente: los costos tardan de 8 a 24 horas en aparecer. Si el presupuesto cruza un umbral, te llegará un correo.

#### Paso 15. Limpieza total
```bash
# 1) Quita el candado (con él puesto no se puede borrar nada)
az lock delete --name no-borrar-lab --resource-group $RG

# 2) Borra el grupo y todo su contenido (tarda unos minutos)
az group delete --name $RG --yes

# 3) Foundry y Key Vault quedan "eliminados temporalmente": púrgalos para liberar los nombres
az cognitiveservices account list-deleted --query "[].name" -o tsv
az cognitiveservices account purge --location $LOC --resource-group $RG --name $AIF
az keyvault list-deleted --resource-type vault --query "[].name" -o tsv
az keyvault purge --name $KV --location $LOC

# 4) Comprueba: debe responder false
az group exists --name $RG
```
- **Explicación:**
  - **Orden:** primero el candado, después el grupo y al final las purgas. La purga solo funciona sobre lo que ya terminó de borrarse.
  - **Si no purgas:**
    - El nombre del recurso de Foundry queda reservado **48 horas**.
    - El de la bóveda queda reservado durante su retención (**7 días** en este laboratorio).
    - Mientras están eliminados, Key Vault no genera uso. Los **despliegues provisionados** de Foundry sí seguirían cobrando hasta purgar (este laboratorio no tiene).
  - **Permisos:**
    - Purgar Foundry requiere *Contributor* (u Owner) **a nivel de suscripción**.
    - Purgar una bóveda requiere ser Owner de la suscripción o tener *Key Vault Purge Operator*.
  - **¿Te arrepentiste?** Antes de purgar puedes recuperar:
    - La bóveda, con `az keyvault recover --name $KV`.
    - El recurso de Foundry, con `az cognitiveservices account recover --location $LOC --resource-group $RG --name $AIF`, dentro de las 48 horas. Recrea primero el grupo de recursos: un grupo borrado no se recupera.
  - **Si ya no usarás la suscripción,** borra también el presupuesto (**Cost Management › Budgets**) y, si creaste una, la cuenta de almacenamiento de Cloud Shell.

---

## 10. Errores comunes y cómo resolverlos

| Mensaje o síntoma | Qué significa | Solución |
|---|---|---|
| `MissingSubscriptionRegistration` | La suscripción no está registrada en ese proveedor | `az provider register --namespace <Proveedor> --wait` ([Paso 4](#paso-4-revisa-los-proveedores-de-recursos)) |
| `AuthorizationFailed` | Te falta un rol de **control** en ese ámbito | `az role assignment list --assignee $YO --all -o table` y pide el rol a un Owner |
| *The operation is not allowed by RBAC* o 403 en Key Vault | Te falta un rol de **datos**, o aún no se propaga | Asigna *Key Vault Secrets User/Officer* y espera unos minutos |
| No puedes crear agentes aunque eres Owner | Owner no tiene `dataActions` | Asígnate **Foundry User** sobre el recurso ([Paso 8](#paso-8-asigna-los-roles-de-foundry)) |
| `CustomDomainInUse` | El subdominio de Foundry ya existe en Azure | Cambia `INI` (o el nombre) y repite |
| Error que pide habilitar una identidad administrada al crear el proyecto | El recurso se creó sin identidad | Crea el recurso con `--assign-identity` |
| No puedes reutilizar el nombre de un recurso de Foundry recién borrado | Eliminación temporal de 48 horas | `az cognitiveservices account purge …` o espera |
| La bóveda "ya existe" aunque la borraste | Eliminación temporal (retención) | `az keyvault purge --name … --location …` o usa otro nombre |
| `ScopeLocked` | Hay un candado en ese ámbito o en uno superior | `az lock list`, y `az lock delete` (requiere Owner o User Access Administrator) |
| `RequestDisallowedByPolicy` | Una Azure Policy lo prohíbe (región, tipo, etiquetas) | Revisa qué política aplica y usa una configuración permitida |
| Cloud Shell no arranca | Falta registrar `Microsoft.CloudShell` | Regístralo ([Paso 2](#paso-2-abre-cloud-shell)) |
| *unrecognized arguments* en comandos de proyectos | CLI desactualizada | `az upgrade` (se requiere 2.80.0 o posterior) |
| Las variables están vacías | La sesión efímera se reinició | Repite el bloque del [Paso 3](#paso-3-define-tus-variables) |

---

### Recursos
- **Fundamentos:**
  - [Fundamentos de Azure (AZ-900) en Microsoft Learn](https://learn.microsoft.com/es-es/training/paths/azure-fundamentals-describe-cloud-concepts/)
  - [Responsabilidad compartida en la nube](https://learn.microsoft.com/es-es/azure/security/fundamentals/shared-responsibility)
  - [¿Qué es Azure Resource Manager?](https://learn.microsoft.com/es-es/azure/azure-resource-manager/management/overview)
  - [Proveedores y tipos de recursos](https://learn.microsoft.com/es-es/azure/azure-resource-manager/management/resource-providers-and-types)
- **Regiones:**
  - [¿Qué son las zonas de disponibilidad?](https://learn.microsoft.com/es-es/azure/reliability/availability-zones-overview)
  - [Pares de regiones y regiones sin par](https://learn.microsoft.com/es-es/azure/reliability/regions-paired)
- **Organización:**
  - [Grupos de administración](https://learn.microsoft.com/es-es/azure/governance/management-groups/overview)
- **Identidad y acceso:**
  - [¿Qué es Azure RBAC?](https://learn.microsoft.com/es-es/azure/role-based-access-control/overview)
  - [RBAC en Microsoft Foundry](https://learn.microsoft.com/es-es/azure/foundry/concepts/rbac-foundry)
  - [Autenticación y autorización en Foundry](https://learn.microsoft.com/es-es/azure/foundry/concepts/authentication-authorization-foundry)
  - [Identidades administradas](https://learn.microsoft.com/es-es/entra/identity/managed-identities-azure-resources/overview)
- **Key Vault:**
  - [Azure RBAC para Key Vault](https://learn.microsoft.com/es-es/azure/key-vault/general/rbac-guide)
  - [Eliminación temporal de Key Vault](https://learn.microsoft.com/es-es/azure/key-vault/general/soft-delete-overview)
- **Gobierno:**
  - [Etiquetas](https://learn.microsoft.com/es-es/azure/azure-resource-manager/management/tag-resources)
  - [Candados](https://learn.microsoft.com/es-es/azure/azure-resource-manager/management/lock-resources)
  - [Azure Policy](https://learn.microsoft.com/es-es/azure/governance/policy/overview)
  - [Reglas de nombres](https://learn.microsoft.com/es-es/azure/azure-resource-manager/management/resource-name-rules)
  - [Convención de nombres del CAF](https://learn.microsoft.com/es-es/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming)
  - [Abreviaturas del CAF](https://learn.microsoft.com/es-es/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations)
- **Costos:**
  - [Crear presupuestos](https://learn.microsoft.com/es-es/azure/cost-management-billing/costs/tutorial-acm-create-budgets)
  - [Costos en Microsoft Foundry](https://learn.microsoft.com/es-es/azure/foundry/concepts/manage-costs)
  - [Calculadora de precios](https://azure.microsoft.com/pricing/calculator/)
- **Herramientas:**
  - [El portal de Azure](https://learn.microsoft.com/es-es/azure/azure-portal/azure-portal-overview)
  - [Cloud Shell: sesiones efímeras](https://learn.microsoft.com/es-es/azure/cloud-shell/get-started/ephemeral)
- **Foundry:**
  - [Crear un proyecto de Foundry](https://learn.microsoft.com/es-es/azure/foundry/how-to/create-projects)
  - [Crear un recurso de Microsoft Foundry con Bicep](https://learn.microsoft.com/es-es/azure/foundry/how-to/create-resource-template)
  - [Recuperar o purgar recursos de Foundry eliminados](https://learn.microsoft.com/es-es/azure/ai-services/recover-purge-resources)
- **Cuentas:**
  - [Cuenta gratuita de Azure](https://azure.microsoft.com/pricing/purchase-options/azure-account)
  - [Azure for Students](https://azure.microsoft.com/free/students/)
