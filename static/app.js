let cy = null;

// Cargar e inicializar el Grafo
async function inicializarGrafo() {
    try {
        const res = await fetch('/api/grafo');
        const elementos = await res.json();

        cy = cytoscape({
            container: document.getElementById('cy'),
            elements: elementos,
            style: [
                {
                    selector: 'node',
                    style: {
                        'background-color': '#fff',
                        'border-width': 2,
                        'border-color': '#000',
                        'label': 'data(label)',
                        'color': '#000',
                        'font-weight': 'bold',
                        'text-valign': 'center',
                        'text-halign': 'center',
                        'width': '30px',
                        'height': '30px'
                    }
                },
                {
                    selector: 'edge',
                    style: {
                        'width': 1.5,
                        'line-color': '#444',
                        'target-arrow-color': '#444',
                        'target-arrow-shape': 'triangle',
                        'curve-style': 'straight',
                        'label': 'data(weight)',
                        'font-size': '11px',
                        'color': '#222',
                        'text-background-opacity': 1,
                        'text-background-color': '#ffffff',
                        'text-background-padding': '2px'
                    }
                },
                {
                    selector: 'edge[?bidirectional]',
                    style: {
                        'source-arrow-color': '#444',
                        'source-arrow-shape': 'triangle'
                    }
                },
                {
                    selector: '.highlighted',
                    style: {
                        'line-color': '#ff0000',
                        'target-arrow-color': '#ff0000',
                        'source-arrow-color': '#ff0000',
                        'border-color': '#ff0000',
                        'background-color': '#ffcccc',
                        'width': 3.5
                    }
                }
            ],
            layout: { name: 'preset' }
        });

        cy.fit();
    } catch (err) {
        console.error("Error inicializando grafo:", err);
    }
}

// Ejecutar búsqueda y actualizar la UI
async function ejecutarBusqueda() {
    const algoritmo = document.getElementById('select-algoritmo').value;
    const sentido = document.getElementById('select-sentido').value;
    const inicio = parseInt(document.getElementById('nodo-inicio').value);
    const fin = parseInt(document.getElementById('nodo-fin').value);

    // Petición a FastAPI
    const response = await fetch('/api/buscar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ algoritmo, sentido, inicio, fin })
    });

    const data = await response.json();
    const ruta = data.ruta; // Arreglo de enteros [1, 6, 16, ...]

    // Desplegar la ruta
    document.getElementById('resultado-ruta').innerText = data.ruta ? data.ruta.join(' ➔ ') : 'Ruta no encontrada';

    // Desplegar la tabla ASCII preservando espacios y saltos de línea
    document.getElementById('contenedor-pasos').textContent = data.pasos;

    // --- C. Resaltar en Cytoscape ---
    if (cy) {
        // Limpiar resaltado anterior
        cy.elements().removeClass('highlighted');

        // Resaltar nodos y conexiones de la ruta
        for (let i = 0; i < ruta.length; i++) {
            const nodoActual = String(ruta[i]);
            cy.getElementById(nodoActual).addClass('highlighted');

            if (i < ruta.length - 1) {
                const nodoSig = String(ruta[i + 1]);
                // Buscar arista en cualquier dirección (u-v o v-u)
                const edge = cy.elements(`edge[source="${nodoActual}"][target="${nodoSig}"], edge[source="${nodoSig}"][target="${nodoActual}"]`);
                if (edge.length) edge.addClass('highlighted');
            }
        }
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    inicializarGrafo();
    document.getElementById('btn-buscar').addEventListener('click', ejecutarBusqueda);
});