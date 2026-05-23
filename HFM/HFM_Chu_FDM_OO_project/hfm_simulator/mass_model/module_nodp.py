# HFM/HFM_Chu_FDM_OO/module_nodp.py

# Import NumPy for numerical operations and array manipulation
# Importa NumPy para operações numéricas e manipulação de arrays
import numpy as np

# Import the base class for hollow fiber membrane modules
# Importa a classe base para módulos de membrana de fibras ocas
from .module_base import BaseHFMModule

# Import sparse matrix constructor used for Jacobian sparsity pattern
# Importa o construtor de matriz esparsa usado para definir a estrutura do Jacobiano
from scipy.sparse import lil_matrix


class HFM_NoDP(BaseHFMModule):
    """
    FDM model of the hollow fiber module.

    SINGLE RESPONSIBILITY:
    - define the model residuals (mass + momentum)
    - DOES NOT solve
    - DOES NOT print
    - DOES NOT know scenarios
    """
    """
    Modelo FDM do módulo de fibras ocas.

    RESPONSABILIDADE ÚNICA:
    - definir os resíduos do modelo (massa + momento)
    - NÃO resolve
    - NÃO imprime
    - NÃO conhece cenários
    """

    def __init__(
        self,
        geometry,
        properties,
        R,
        T,
        Permeance,
        # K_shell, # no pressure drop
        # K_bore, # no pressure drop
        n_comp,
        FFeed,
        PFeed,
        PPerm,
    ):
        """
        Parameters
        ----------
        geometry : Geometry
            Module geometry object
            Objeto com a geometria do módulo
        properties : MixtureProperties
            Physical properties adapter
            Adaptador de propriedades físicas
        R : float
            Gas constant
            Constante dos gases
        T : float
            Temperature [K]
            Temperatura [K]
        Permeance : array
            Permeabilities per component
            Permeabilidades por componente
        K_shell : float
            Shell hydraulic constant
            Constante hidráulica do casco
        K_bore : float
            Bore hydraulic constant
            Constante hidráulica do bore
        n_comp : int
            Number of components
            Número de componentes
        FFeed : array
            Feed molar flow rate per component
            Vazão molar de alimentação por componente
        PFeed : float
            Retentate inlet pressure
            Pressão de entrada do retentado
        PPerm : float
            Permeate outlet pressure
            Pressão de saída do permeado
        """

        # Store geometry object (contains discretization and membrane area)
        # Armazena o objeto de geometria (contém discretização e área da membrana)
        self.geom = geometry

        # Store mixture physical properties handler
        # Armazena o manipulador de propriedades físicas da mistura
        self.props = properties

        # Universal gas constant
        # Constante universal dos gases
        self.R = R

        # Operating temperature
        # Temperatura de operação
        self.T = T

        # Permeability of each component through the membrane
        # Permeabilidade de cada componente através da membrana
        self.Permeance = Permeance

        # Pressure drop coefficients are NOT used in this model
        # Coeficientes de queda de pressão NÃO são usados neste modelo
        # self.K_shell = K_shell
        # self.K_bore = K_bore

        # Number of components in the gas mixture
        # Número de componentes na mistura gasosa
        self.nc = n_comp

        # Feed molar flow rate per component
        # Vazão molar de alimentação por componente
        self.FFeed = FFeed

        # Retentate inlet pressure
        # Pressão de entrada do retentado
        self.PFeed = PFeed

        # Permeate outlet pressure
        # Pressão de saída do permeado
        self.PPerm = PPerm


    def residuals(self, x):

        # Number of spatial segments
        # Número de segmentos espaciais
        NCells = self.geom.NCells

        # Number of components
        # Número de componentes
        nc = self.nc

        # Axial discretization step
        # Passo de discretização axial
        dz = self.geom.dz

        # Membrane area per segment
        # Área de membrana por segmento
        AREA = self.geom.AREA_SEG

        # Number of variables per spatial node
        # Número de variáveis por nó espacial
        width = 2 * nc + 2

        # Reshape the solver vector into matrix form (nodes × variables)
        # Reorganiza o vetor do solver em forma matricial (nós × variáveis)
        X = x.reshape((NCells + 1, width))

        # Retentate component molar flows
        # Vazões molares por componente no retentado
        FRet_Comp = X[:, :nc]

        # Permeate component molar flows
        # Vazões molares por componente no permeado
        FPerm_Comp = X[:, nc:2 * nc]

        # Retentate pressure
        # Pressão do retentado
        PRetCell = X[:, 2 * nc]

        # Permeate pressure
        # Pressão do permeado
        PPermCell = X[:, 2 * nc + 1]

        # Small number to avoid division by zero
        # Pequeno número para evitar divisão por zero
        eps = 1e-12

        # Reference flow used for residual scaling
        # Vazão de referência usada para escalar os resíduos
        Fref = max(np.sum(self.FFeed), eps)

        # Total retentate flow
        # Vazão total do retentado
        SumFRet_Comp = FRet_Comp.sum(axis=1)

        # Total permeate flow
        # Vazão total do permeado
        SumFPerm_Comp = FPerm_Comp.sum(axis=1)

        # Precompute inverse values for numerical efficiency
        # Pré-calcula inversos para melhorar eficiência numérica
        invSumFRet_Comp = 1 / np.maximum(SumFRet_Comp, eps)
        invSumFPerm_Comp = 1 / np.maximum(SumFPerm_Comp, eps)

        # Total number of residual equations
        # Número total de equações residuais
        nR = 2*nc + 2 + NCells*(2*nc + 2)

        # Initialize residual vector
        # Inicializa vetor de resíduos
        Res_Vec = np.zeros(nR)

        # Residual index pointer
        # Ponteiro de índice do vetor de resíduos
        i = 0

        # ===============================
        # Boundary conditions
        # Condições de contorno
        # ===============================

        # Feed composition condition
        # Condição de composição da alimentação
        Res_Vec[i:i+nc] = (FRet_Comp[0] - self.FFeed)/Fref
        i += nc

        # Retentate inlet pressure condition
        # Condição da pressão de entrada do retentado
        Res_Vec[i] = (PRetCell[0] - self.PFeed)/self.PFeed
        i += 1

        # Permeate outlet pressure condition
        # Condição da pressão de saída do permeado
        Res_Vec[i] = (PPermCell[0] - self.PPerm)/self.PPerm
        i += 1

        # Zero permeate flow at module end
        # Fluxo zero no permeado no final do módulo
        Res_Vec[i:i+nc] = (FPerm_Comp[NCells])/Fref
        i += nc

        # ===============================
        # Axial discretization loop
        # Loop axial da discretização
        # ===============================

        for k in range(1, NCells+1):

            # Previous node index
            # Índice do nó anterior
            km = k-1

            # Retentate compositions
            # Composição do retentado
            ZRet_k = FRet_Comp[k] * invSumFRet_Comp[k]
            ZRet_km = FRet_Comp[km] * invSumFRet_Comp[km]

            # Permeate compositions
            # Composição do permeado
            ZPerm_k = FPerm_Comp[k] * invSumFPerm_Comp[k]
            ZPerm_km = FPerm_Comp[km] * invSumFPerm_Comp[km]

            # At last node permeate composition is undefined
            # No último nó a composição do permeado é indefinida
            if k==NCells:
                ZPerm_k[:] = 0

            # Viscosity is not required because pressure drop is ignored
            # Viscosidade não é necessária pois a queda de pressão é ignorada
            # mu_f = self.props.viscosity(...)
            # mu_g = self.props.viscosity(...)

            # Membrane permeation driving force
            # Força motriz da permeação na membrana
            FMemb = self.Permeance * AREA * (PRetCell[k]*ZRet_k - PPermCell[km]*ZPerm_km)

            # Retentate mass balance
            # Balanço de massa no retentado
            Res_Vec[i:i+nc] = (FRet_Comp[k] - FRet_Comp[km] + FMemb)/Fref
            i += nc

            # Permeate mass balance
            # Balanço de massa no permeado
            if k < NCells:
                Res_Vec[i:i+nc] = (FPerm_Comp[km] - FPerm_Comp[k] - FMemb)/Fref
            else:
                Res_Vec[i:i+nc] = (FPerm_Comp[km] - FMemb)/Fref

            i += nc

            # Pressure drop terms removed
            # Termos de queda de pressão removidos
            # dP = ...
            # dp = ...

            # Retentate pressure remains constant along module
            # Pressão do retentado permanece constante ao longo do módulo
            Res_Vec[i] = (PRetCell[km] - PRetCell[k])/self.PFeed
            i += 1

            # Permeate pressure remains constant
            # Pressão do permeado permanece constante
            Res_Vec[i] = (PPermCell[k] - PPermCell[km])/self.PPerm
            i += 1

        return Res_Vec



    def build_jac_sparsity(self):

        # Number of nodes
        # Número de nós
        NCells = self.geom.NCells

        # Number of components
        # Número de componentes
        nc = self.nc

        # Variables per node
        # Variáveis por nó
        width = 2*nc + 2

        # Total number of variables
        # Número total de variáveis
        nvar = (NCells+1)*width

        # Total number of equations
        # Número total de equações
        neq  = 2*nc + 2 + NCells*(2*nc + 2)

        # Sparse Jacobian structure initialization
        # Inicialização da estrutura esparsa do Jacobiano
        Spa_Mat = lil_matrix((neq, nvar), dtype=int)

        # Row index counter
        # Contador de linhas
        row = 0

        # Boundary conditions sparsity pattern
        # Estrutura esparsa das condições de contorno
        for j in range(nc):
            Spa_Mat[row, j] = 1
            row += 1

        Spa_Mat[row, 2*nc] = 1
        row += 1

        Spa_Mat[row, 2*nc+1] = 1
        row += 1

        base = NCells*width

        for j in range(nc):
            Spa_Mat[row, base+nc+j] = 1
            row += 1

        # Interior nodes sparsity pattern
        # Estrutura esparsa dos nós internos
        for k in range(1, NCells+1):

            base_k  = k*width
            base_km = (k-1)*width

            for _ in range(2*nc+2):

                # Dependence on current node variables
                # Dependência das variáveis do nó atual
                Spa_Mat[row, base_k:base_k+width] = 1

                # Dependence on previous node variables
                # Dependência das variáveis do nó anterior
                Spa_Mat[row, base_km:base_km+width] = 1

                row += 1

        # Convert to CSR format for efficient solver usage
        # Converte para formato CSR para uso eficiente no solver
        return Spa_Mat.tocsr()