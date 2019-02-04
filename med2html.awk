function title(label){
    switch(label) {
    case "spec": return "Eventi Speciali";
    case "hal": return "Halloween";
    case "nat": return "Natale";
    case "mi": return "Mezzogiorno d'Inchiostro";
    case "fdi": return "Ferragosto d'Inchiostro";
    case "anno": return "Annuale";
    case "normale": return "Normale";
    case "lune": return "Lune";
    case "mr": return "Migliori racconti";
    case "ps": return "Penna & Spada";
    default: return label;
    }
}

BEGIN { prevtype=""; prevsub=""; prevyear=""; }
$1 != prevtype {
    if (prevtype!="") {
	printf("            </table>\n");
	printf("        </section>\n");
	printf("    </section>\n");
	printf("</section>\n");
    }
    prevtype=$1;
    prevsub="";
    prevyear="";
    printf("<section class='type'>\n");
    printf("    <h1>%s</h1>\n",title(prevtype));
}
$2 != prevsub {
    if (prevsub!="") {
	printf("            </table>\n");
	printf("        </section>\n");
	printf("    </section>\n");
    }
    prevsub=$2;
    prevyear="";
    printf("    <section class='sub'>\n");
    printf("        <h2>%s</h2>\n",title(prevsub));
}
$3 != prevyear {
    if (prevyear!="") {
	printf("            </table>\n");
	printf("        </section>\n");
    }
    prevyear=$3;
    printf("        <section class='year'>\n");
    if (prevyear!="----") printf("            <h3>%s</h3>\n",prevyear);
    printf("            <table>\n");
}
{
    printf("                <tr>\n");
    printf("                    <td><img src='./%s'/></td>\n",$4);
    printf("                    <td>https://simplehtml.mygor.xyz/wd/medagliette/%s</td>\n",$4);
    printf("                </tr>\n");
}
END {
    printf("            </table>\n");
    printf("        </section>\n");
    printf("    </section>\n");
    printf("</section>\n");
}
